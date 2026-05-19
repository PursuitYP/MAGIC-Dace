"""Markov transition matrix core + the three Table-4 initialization modes.

Mode semantics (see MAJIC paper Table 4):

* ``uniform``        -- MAJIC(-Init): M_ij = 1/K + dynamic Q-learning update.
* ``learned``        -- Full MAJIC:   load learned M + dynamic Q-learning update.
* ``learned_static`` -- MAJIC(-DynUpd): load learned M, freeze (no update, no reset).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import numpy as np


# Default hyper-parameters (match upstream markov_methods/markov_attack_api_dynamic.py)
DEFAULT_GAMMA = 0.5
DEFAULT_ALPHA = 0.1
DEFAULT_BETA = 0.01
DEFAULT_TEMPERATURE = 0.15
DEFAULT_DECAY_ETA = 0.95
DEFAULT_DECAY_INTERVAL = 40
DEFAULT_RESET_INTERVAL = 80
SUCCESS_REWARD = 1.0
FAIL_REWARD = 0.0


INIT_MODES = ("uniform", "learned", "learned_static")


def softmax_row(x_row: np.ndarray, temperature: float = DEFAULT_TEMPERATURE) -> np.ndarray:
    if temperature <= 0:
        raise ValueError("Temperature must be positive.")
    if x_row.ndim != 1:
        raise ValueError("softmax_row expects a 1D array.")
    if x_row.size == 0:
        return x_row
    adj = x_row / temperature
    max_val = np.max(adj)
    e_x = np.exp(adj - max_val)
    denom = np.sum(e_x)
    if denom == 0:
        return np.ones_like(adj) / adj.size
    return e_x / denom


def softmax_normalize_with_temperature(ratios, temperature: float = 1.0) -> np.ndarray:
    if temperature <= 0:
        raise ValueError("Temperature must be > 0.")
    ratios = np.asarray(ratios, dtype=np.float64)
    exp_r = np.exp(ratios / temperature)
    return exp_r / np.sum(exp_r)


@dataclass
class MatrixController:
    """Holds the Markov matrix + implements the three init modes.

    Use ``MatrixController.build(mode=...)`` as the factory.
    """

    matrix: np.ndarray
    mode: str
    k: int
    alpha: float = DEFAULT_ALPHA
    gamma: float = DEFAULT_GAMMA
    beta: float = DEFAULT_BETA
    temperature: float = DEFAULT_TEMPERATURE
    decay_eta: float = DEFAULT_DECAY_ETA
    decay_interval: int = DEFAULT_DECAY_INTERVAL
    reset_interval: int = DEFAULT_RESET_INTERVAL

    # --- factories ---------------------------------------------------------
    @classmethod
    def build(
        cls,
        *,
        mode: str,
        k: int = 10,
        init_matrix_path: Optional[str] = None,
        alpha: float = DEFAULT_ALPHA,
        gamma: float = DEFAULT_GAMMA,
        beta: float = DEFAULT_BETA,
        temperature: float = DEFAULT_TEMPERATURE,
        decay_eta: float = DEFAULT_DECAY_ETA,
        decay_interval: int = DEFAULT_DECAY_INTERVAL,
        reset_interval: int = DEFAULT_RESET_INTERVAL,
    ) -> "MatrixController":
        if mode not in INIT_MODES:
            raise ValueError(f"Unknown MAJIC_INIT_MODE={mode}; must be one of {INIT_MODES}.")

        if mode == "uniform":
            matrix = np.full((k, k), 1.0 / k, dtype=np.float64)
        else:
            if not init_matrix_path:
                raise ValueError(
                    f"mode={mode} requires init_matrix_path. Run "
                    "`python -m majic_eval.build_init_matrix` to create one, "
                    "or pass MAJIC_INIT_MATRIX=/path/to/10x10.npy."
                )
            if not os.path.exists(init_matrix_path):
                raise FileNotFoundError(
                    f"init_matrix_path not found: {init_matrix_path}. "
                    "Run `python -m majic_eval.build_init_matrix` to generate it."
                )
            matrix = np.load(init_matrix_path).astype(np.float64)
            if matrix.shape != (k, k):
                raise ValueError(
                    f"Loaded matrix shape {matrix.shape} != expected ({k}, {k})."
                )

        return cls(
            matrix=matrix,
            mode=mode,
            k=k,
            alpha=alpha,
            gamma=gamma,
            beta=beta,
            temperature=temperature,
            decay_eta=decay_eta,
            decay_interval=decay_interval,
            reset_interval=reset_interval,
        )

    # --- properties --------------------------------------------------------
    @property
    def updates_enabled(self) -> bool:
        """Whether Q-learning updates / decay / reset are applied."""
        return self.mode in ("uniform", "learned")

    def initial_vector(self) -> np.ndarray:
        """Selection probabilities for the first strategy of each chain."""
        column_sums = np.sum(self.matrix, axis=0)
        return softmax_normalize_with_temperature(column_sums, temperature=1.0)

    # --- mutations ---------------------------------------------------------
    def update_on_feedback(
        self,
        prev_idx_1based: int,
        current_idx_1based: int,
        reward: float,
    ) -> None:
        """Q-learning-style update (paper Eq. (4)) + softmax renormalization.

        No-op for ``learned_static`` mode.
        """
        if not self.updates_enabled:
            return
        prev_idx = prev_idx_1based - 1
        current_idx = current_idx_1based - 1
        if not (0 <= prev_idx < self.k and 0 <= current_idx < self.k):
            print(f"[markov] bad indices prev={prev_idx_1based}, cur={current_idx_1based}; skip.")
            return

        current_prob_ij = self.matrix[prev_idx, current_idx]
        max_prob_next_state = float(np.max(self.matrix[current_idx, :]))
        q_target = reward + self.gamma * max_prob_next_state
        new_logit = current_prob_ij + self.alpha * (q_target - current_prob_ij)

        row = self.matrix[prev_idx, :].copy()
        row[current_idx] = new_logit
        self.matrix[prev_idx, :] = softmax_row(row, temperature=self.temperature)

    def apply_periodic_schedule(self, total_queries: int) -> None:
        """Apply adaptive decay of alpha and periodic partial reset of M.

        No-op for ``learned_static`` mode.
        """
        if not self.updates_enabled:
            return
        if total_queries <= 0:
            return
        if total_queries % self.decay_interval == 0:
            self.alpha *= self.decay_eta
        if total_queries % self.reset_interval == 0:
            uniform = np.full_like(self.matrix, 1.0 / self.k)
            self.matrix = (1.0 - self.beta) * self.matrix + self.beta * uniform

    # --- sampling helpers --------------------------------------------------
    def sample_next(self, failed_idx_1based: int, rng: np.random.Generator) -> int:
        row = self.matrix[failed_idx_1based - 1, :]
        total = float(np.sum(row))
        if total <= 0 or not np.isfinite(total):
            probs = np.full(self.k, 1.0 / self.k)
        else:
            probs = row / total
        choice_0based = int(rng.choice(self.k, p=probs))
        return choice_0based + 1

    def sample_initial(self, rng: np.random.Generator) -> int:
        v = self.initial_vector()
        total = float(np.sum(v))
        if total <= 0 or not np.isfinite(total):
            v = np.full(self.k, 1.0 / self.k)
        else:
            v = v / total
        return int(rng.choice(self.k, p=v)) + 1

    # --- serialization -----------------------------------------------------
    def snapshot(self) -> dict:
        return {
            "mode": self.mode,
            "alpha": self.alpha,
            "gamma": self.gamma,
            "beta": self.beta,
            "temperature": self.temperature,
            "matrix": self.matrix.round(6).tolist(),
        }
