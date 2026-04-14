### dace: Bayesian adversarial replay pool with strategy coverage tracking ###
"""
Unified archive pool for attack diversity reward computation and Bayesian replay.

The pool stores successful attack prompts with:
- Strategy descriptor (risk_category, attack_style) for diversity tracking
- Beta-Bernoulli posterior (successes, failures) for Thompson Sampling replay
"""

import json
import re
import hashlib
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import numpy as np


@dataclass
class ArchiveEntry:
    """Single entry in the unified archive / replay pool."""

    prompt_text: str  # Attacker's rewritten prompt (extracted from <answer>)
    seed_prompt: str  # Original vanilla prompt
    data_type: str  # 'vanilla_harmful' or 'vanilla_benign'
    strategy: Tuple[int, int]  # (risk_category_idx, attack_style_idx)
    extra_info: dict  # Preserved extra_info from the training sample
    successes: float  # Beta posterior s_i (float to support decay)
    failures: float  # Beta posterior f_i
    step_added: int  # Global step when first added
    prompt_data: dict  # Full fields to reconstruct a DataProto row for replay
    # Expected prompt_data keys: question, data_source, data_type, prompt,
    #   adversarial, reward_model, extra_info, ability, seed_prompt,
    #   input_template, attacker_template


### dace: strategy space constants matching preprocess_dace.py ###
RISK_CATEGORIES = [
    "Violent Crimes",
    "Non-Violent Crimes",
    "Sex-Related Crimes",
    "Child Sexual Exploitation",
    "Defamation",
    "Specialized Advice",
    "Privacy",
    "Intellectual Property",
    "Indiscriminate Weapons",
    "Hate",
    "Suicide & Self-Harm",
    "Sexual Content",
    "Elections",
    "Code Interpreter Abuse",
]  # |S| = 14

ATTACK_STYLES = [
    "Slang",
    "Technical Terms",
    "Role Play",
    "Authority Manipulation",
    "Misspellings",
    "Word Play",
    "Emotional Manipulation",
    "Hypotheticals",
    "Historical Scenario",
    "Uncommon Dialects",
]  # |C| = 10

# Build lookup dicts for fuzzy matching (lowercase -> index)
_RISK_LOOKUP: Dict[str, int] = {cat.lower(): i for i, cat in enumerate(RISK_CATEGORIES)}
_STYLE_LOOKUP: Dict[str, int] = {sty.lower(): i for i, sty in enumerate(ATTACK_STYLES)}

N_RISK = len(RISK_CATEGORIES)
N_STYLE = len(ATTACK_STYLES)
N_SLOTS = N_RISK * N_STYLE  # 140


class ArchivePool:
    """Unified archive pool for diversity reward + Bayesian replay.

    Maintains:
    - entries: list of ArchiveEntry
    - slot_counts: (N_RISK, N_STYLE) frequency array for coverage computation
    - prompt_hash_set: set of prompt text hashes for O(1) dedup
    - _cached_max_delta: cached denominator for coverage reward (invalidated on mutation)
    """

    N_RISK = N_RISK
    N_STYLE = N_STYLE
    N_SLOTS = N_SLOTS

    def __init__(self, config=None):
        config = config or {}
        self.entries: List[ArchiveEntry] = []
        self.prompt_hash_set: Set[str] = set()
        self.prompt_hash_to_idx: Dict[str, int] = {}  # hash -> entry index
        self.slot_counts: np.ndarray = np.zeros((N_RISK, N_STYLE), dtype=np.float64)

        # Config
        self.gamma_decay: float = float(config.get('gamma_decay', 0.90))
        self.prune_threshold: float = float(config.get('prune_threshold', 0.20))
        self.prune_min_trials: float = float(config.get('prune_min_trials', 3.0))
        self.max_pool_size: int = int(config.get('max_pool_size', 5000))
        self.alpha_prior: float = float(config.get('alpha_prior', 1.0))
        self.beta_prior: float = float(config.get('beta_prior', 1.0))
        self.epsilon: float = float(config.get('epsilon', 1e-8))

        # Cache for diversity reward denominator
        self._cached_max_delta: Optional[float] = None

    # ──────────────────────────────────────────────────────────────
    # Strategy extraction
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def extract_strategy(text: str) -> Optional[Tuple[int, int]]:
        """Parse <strategy> tags and return (risk_idx, style_idx) or None."""
        if not text:
            return None
        pattern = r'<strategy>\s*risk category:\s*(.+?)\s*\n\s*attack style:\s*(.+?)\s*</strategy>'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if not match:
            return None
        risk_str = match.group(1).strip().lower()
        style_str = match.group(2).strip().lower()
        risk_idx = _RISK_LOOKUP.get(risk_str)
        style_idx = _STYLE_LOOKUP.get(style_str)
        if risk_idx is None or style_idx is None:
            # Try substring matching as fallback
            if risk_idx is None:
                for key, idx in _RISK_LOOKUP.items():
                    if key in risk_str or risk_str in key:
                        risk_idx = idx
                        break
            if style_idx is None:
                for key, idx in _STYLE_LOOKUP.items():
                    if key in style_str or style_str in key:
                        style_idx = idx
                        break
        if risk_idx is None or style_idx is None:
            return None
        return (risk_idx, style_idx)

    # ──────────────────────────────────────────────────────────────
    # Entropy computation
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def _compute_entropy(counts: np.ndarray) -> float:
        """Shannon entropy H(p) where p = counts / sum(counts). H = -sum(p_i * log(p_i))."""
        total = counts.sum()
        if total <= 0:
            return 0.0
        p = counts.flatten() / total
        mask = p > 0
        if not mask.any():
            return 0.0
        return -float(np.sum(p[mask] * np.log(p[mask])))

    def compute_coverage_entropy(self) -> float:
        """Public method: current strategy distribution entropy."""
        return self._compute_entropy(self.slot_counts)

    # ──────────────────────────────────────────────────────────────
    # Diversity reward: Normalized Marginal Coverage Gain
    # ──────────────────────────────────────────────────────────────

    def _compute_marginal_entropy_gain(self, strategy: Tuple[int, int]) -> float:
        """H(p_{A ∪ {x}}) - H(p_A) for a hypothetical sample at given slot."""
        current_H = self._compute_entropy(self.slot_counts)
        tmp = self.slot_counts.copy()
        tmp[strategy[0], strategy[1]] += 1.0
        new_H = self._compute_entropy(tmp)
        return new_H - current_H

    def _compute_max_marginal_gain(self) -> float:
        """max_b [ H(p_{A ∪ {x_b}}) - H(p_A) ] over all slots. Cached."""
        if self._cached_max_delta is not None:
            return self._cached_max_delta
        current_H = self._compute_entropy(self.slot_counts)
        max_delta = 0.0
        for r in range(N_RISK):
            for s in range(N_STYLE):
                tmp = self.slot_counts.copy()
                tmp[r, s] += 1.0
                delta = self._compute_entropy(tmp) - current_H
                if delta > max_delta:
                    max_delta = delta
        self._cached_max_delta = max_delta
        return max_delta

    def compute_diversity_reward(self, strategy: Tuple[int, int]) -> float:
        """Normalized Marginal Coverage Gain.

        R_div(x) = [H(p_{A∪{x}}) - H(p_A)] / [max_b(H(p_{A∪{x_b}}) - H(p_A)) + ε]
        """
        delta = self._compute_marginal_entropy_gain(strategy)
        delta_max = self._compute_max_marginal_gain()
        return delta / (delta_max + self.epsilon)

    def _invalidate_cache(self):
        self._cached_max_delta = None

    # ──────────────────────────────────────────────────────────────
    # Pool mutation: add, decay, prune
    # ──────────────────────────────────────────────────────────────

    @staticmethod
    def _prompt_hash(text: str) -> str:
        return hashlib.md5(text.encode('utf-8', errors='replace')).hexdigest()

    def add_entry(self, entry: ArchiveEntry) -> bool:
        """Add successful attack to pool. Returns True if new entry, False if duplicate.

        For duplicates, increments existing entry's successes.
        """
        h = self._prompt_hash(entry.prompt_text)
        if h in self.prompt_hash_set:
            idx = self.prompt_hash_to_idx.get(h)
            if idx is not None and idx < len(self.entries):
                self.entries[idx].successes += 1.0
            return False

        # New entry
        self.prompt_hash_set.add(h)
        idx = len(self.entries)
        self.prompt_hash_to_idx[h] = idx
        self.entries.append(entry)
        r, s = entry.strategy
        self.slot_counts[r, s] += 1.0
        self._invalidate_cache()

        # Enforce max size: drop entry with lowest posterior mean
        if len(self.entries) > self.max_pool_size:
            self._drop_lowest_value_entry()

        return True

    def _drop_lowest_value_entry(self):
        """Remove the entry with the lowest posterior mean to enforce max_pool_size."""
        if not self.entries:
            return
        worst_idx = min(
            range(len(self.entries)),
            key=lambda i: (self.alpha_prior + self.entries[i].successes)
            / (self.alpha_prior + self.entries[i].successes + self.beta_prior + self.entries[i].failures),
        )
        self._remove_entry_at(worst_idx)

    def _remove_entry_at(self, idx: int):
        """Remove entry at given index and update all tracking structures."""
        entry = self.entries[idx]
        r, s = entry.strategy
        self.slot_counts[r, s] = max(0.0, self.slot_counts[r, s] - 1.0)
        h = self._prompt_hash(entry.prompt_text)
        self.prompt_hash_set.discard(h)
        self.prompt_hash_to_idx.pop(h, None)
        self.entries.pop(idx)
        # Rebuild hash -> idx mapping after removal
        self.prompt_hash_to_idx = {
            self._prompt_hash(e.prompt_text): i for i, e in enumerate(self.entries)
        }
        self._invalidate_cache()

    def time_decay(self):
        """Decay all entries: s_i *= gamma, f_i *= gamma."""
        for entry in self.entries:
            entry.successes *= self.gamma_decay
            entry.failures *= self.gamma_decay
        self._invalidate_cache()

    def prune(self):
        """Remove entries where p_hat < threshold and (s+f) > n_min."""
        to_remove = []
        for i, entry in enumerate(self.entries):
            total = self.alpha_prior + entry.successes + self.beta_prior + entry.failures
            p_hat = (self.alpha_prior + entry.successes) / total if total > 0 else 0.5
            trials = entry.successes + entry.failures
            if p_hat < self.prune_threshold and trials > self.prune_min_trials:
                to_remove.append(i)
        # Remove in reverse order to preserve indices
        for idx in reversed(to_remove):
            self._remove_entry_at(idx)
        if to_remove:
            print(f"[ArchivePool] Pruned {len(to_remove)} entries, remaining: {len(self.entries)}")

    # ──────────────────────────────────────────────────────────────
    # Thompson Sampling
    # ──────────────────────────────────────────────────────────────

    def thompson_sample(self, n: int) -> List[Tuple[int, ArchiveEntry]]:
        """Sample n entries via Thompson Sampling from Beta(alpha+s_i, beta+f_i).

        Returns list of (entry_index, entry) sorted by sampled probability descending.
        """
        if not self.entries or n <= 0:
            return []
        n = min(n, len(self.entries))
        sampled_probs = np.array([
            np.random.beta(self.alpha_prior + e.successes, self.beta_prior + e.failures)
            for e in self.entries
        ])
        top_indices = np.argsort(sampled_probs)[::-1][:n]
        return [(int(idx), self.entries[idx]) for idx in top_indices]

    # ──────────────────────────────────────────────────────────────
    # Posterior update
    # ──────────────────────────────────────────────────────────────

    def update_posterior(self, entry_idx: int, any_harmful: bool):
        """Update Beta posterior after replay rollout.

        If any of G rollouts produced harmful response -> s_j += 1, else f_j += 1.
        """
        if entry_idx < 0 or entry_idx >= len(self.entries):
            return
        if any_harmful:
            self.entries[entry_idx].successes += 1.0
        else:
            self.entries[entry_idx].failures += 1.0

    # ──────────────────────────────────────────────────────────────
    # Checkpoint save / load
    # ──────────────────────────────────────────────────────────────

    def save(self, path):
        """Serialize archive pool to JSON."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            'config': {
                'gamma_decay': self.gamma_decay,
                'prune_threshold': self.prune_threshold,
                'prune_min_trials': self.prune_min_trials,
                'max_pool_size': self.max_pool_size,
                'alpha_prior': self.alpha_prior,
                'beta_prior': self.beta_prior,
                'epsilon': self.epsilon,
            },
            'entries': [
                {
                    'prompt_text': e.prompt_text,
                    'seed_prompt': e.seed_prompt,
                    'data_type': e.data_type,
                    'strategy': list(e.strategy),
                    'extra_info': e.extra_info,
                    'successes': e.successes,
                    'failures': e.failures,
                    'step_added': e.step_added,
                    'prompt_data': e.prompt_data,
                }
                for e in self.entries
            ],
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[ArchivePool] Saved {len(self.entries)} entries to {path}")

    @classmethod
    def load(cls, path, config=None) -> 'ArchivePool':
        """Load archive pool from JSON checkpoint."""
        path = Path(path)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        saved_config = data.get('config', {})
        if config:
            saved_config.update(config)
        pool = cls(saved_config)
        for item in data.get('entries', []):
            entry = ArchiveEntry(
                prompt_text=item['prompt_text'],
                seed_prompt=item['seed_prompt'],
                data_type=item['data_type'],
                strategy=tuple(item['strategy']),
                extra_info=item.get('extra_info', {}),
                successes=float(item['successes']),
                failures=float(item['failures']),
                step_added=int(item.get('step_added', 0)),
                prompt_data=item.get('prompt_data', {}),
            )
            h = cls._prompt_hash(entry.prompt_text)
            pool.prompt_hash_set.add(h)
            pool.prompt_hash_to_idx[h] = len(pool.entries)
            pool.entries.append(entry)
            r, s = entry.strategy
            pool.slot_counts[r, s] += 1.0
        pool._invalidate_cache()
        print(f"[ArchivePool] Loaded {len(pool.entries)} entries from {path}")
        return pool

    def __len__(self) -> int:
        return len(self.entries)

    def __repr__(self) -> str:
        n_occupied = int((self.slot_counts > 0).sum())
        return (
            f"ArchivePool(entries={len(self.entries)}, "
            f"slots_occupied={n_occupied}/{N_SLOTS}, "
            f"entropy={self.compute_coverage_entropy():.3f})"
        )
