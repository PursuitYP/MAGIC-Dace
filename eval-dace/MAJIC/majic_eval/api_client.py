"""OpenAI-compatible API clients for MAJIC (attacker / defender / judge).

Matches the credential precedence used by `OpenRT/unified_eval.py`:
CLI flag -> per-role env var -> generic OPENAI_* fallback.  The attacker
backend is model-agnostic (Qwen / Llama / Mistral) -- we only speak Chat
Completions.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import List, Optional

try:
    from openai import OpenAI
except ImportError as exc:  # pragma: no cover - runtime import guard
    raise ImportError(
        "openai package is required. Activate the OpenRT conda env or "
        "`pip install openai>=1.0`."
    ) from exc


# ---------- Attacker <answer>...</answer> extraction -----------------------
def extract_attacker_answer(text: Optional[str]) -> Optional[str]:
    """Mirror of OpenRT/unified_eval.py::extract_attacker_answer."""
    if text is None:
        return text
    content = str(text)
    start_tag = "<answer>"
    end_tag = "</answer>"
    start_index = content.find(start_tag)
    if start_index == -1:
        return content
    start_index += len(start_tag)
    end_index = content.find(end_tag, start_index)
    if end_index != -1:
        return content[start_index:end_index].strip()
    return content[start_index:].strip()


@dataclass
class APIConfig:
    api_key: str
    base_url: str
    model: str
    role: str  # "attacker" | "defender" | "judge"


class ChatClient:
    """Thin OpenAI-compatible chat wrapper with retry + backoff."""

    def __init__(
        self,
        cfg: APIConfig,
        *,
        temperature: float = 0.0,
        max_tokens: int = 1024,
        max_retries: int = 3,
        retry_sleep: float = 2.0,
        extract_answer: bool = False,
    ) -> None:
        self.cfg = cfg
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries
        self.retry_sleep = retry_sleep
        self.extract_answer = extract_answer
        self._client = OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)

    def chat(
        self,
        messages: List[dict],
        *,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        temp = self.temperature if temperature is None else temperature
        tokens = self.max_tokens if max_tokens is None else max_tokens
        last_err: Optional[Exception] = None
        for attempt in range(self.max_retries):
            try:
                resp = self._client.chat.completions.create(
                    model=self.cfg.model,
                    messages=messages,
                    temperature=temp,
                    max_tokens=tokens,
                )
                content = resp.choices[0].message.content or ""
                if self.extract_answer:
                    content = extract_attacker_answer(content) or ""
                return content
            except Exception as exc:  # noqa: BLE001 - propagate after retries
                last_err = exc
                wait = self.retry_sleep * (attempt + 1)
                print(
                    f"[{self.cfg.role}] API error on attempt {attempt + 1}/"
                    f"{self.max_retries}: {exc}. Retrying in {wait:.1f}s..."
                )
                time.sleep(wait)
        print(f"[{self.cfg.role}] API failed after {self.max_retries} retries: {last_err}")
        return f"API_ERROR: {last_err}"


# ---------- Credential resolution -----------------------------------------
def _resolve(primary: Optional[str], env_name: str, fallback_env: str = "") -> str:
    if primary:
        return primary
    val = os.environ.get(env_name, "")
    if val:
        return val
    if fallback_env:
        return os.environ.get(fallback_env, "")
    return ""


def build_clients(
    *,
    attacker_key: Optional[str] = None,
    attacker_url: Optional[str] = None,
    attacker_model: Optional[str] = None,
    defender_key: Optional[str] = None,
    defender_url: Optional[str] = None,
    defender_model: Optional[str] = None,
    judge_key: Optional[str] = None,
    judge_url: Optional[str] = None,
    judge_model: Optional[str] = None,
    attacker_temperature: float = 0.9,
    defender_temperature: float = 0.0,
    judge_temperature: float = 0.0,
    attacker_max_tokens: int = 1024,
    defender_max_tokens: int = 512,
    judge_max_tokens: int = 32,
    attacker_extract_answer: bool = False,
) -> tuple[ChatClient, ChatClient, ChatClient]:
    """Assemble attacker / defender / judge clients from args + env."""
    a_cfg = APIConfig(
        api_key=_resolve(attacker_key, "ATTACKER_API_KEY", "OPENAI_API_KEY"),
        base_url=_resolve(attacker_url, "ATTACKER_API_BASE_URL", "OPENAI_BASE_URL"),
        model=attacker_model or os.environ.get("ATTACKER_API_MODEL", ""),
        role="attacker",
    )
    d_cfg = APIConfig(
        api_key=_resolve(defender_key, "DEFENDER_API_KEY", "OPENAI_API_KEY"),
        base_url=_resolve(defender_url, "DEFENDER_API_BASE_URL", "OPENAI_BASE_URL"),
        model=defender_model or os.environ.get("DEFENDER_API_MODEL", ""),
        role="defender",
    )
    j_cfg = APIConfig(
        api_key=_resolve(judge_key, "OPENAI_API_KEY"),
        base_url=_resolve(judge_url, "OPENAI_BASE_URL"),
        model=judge_model or os.environ.get("JUDGE_API_MODEL", "gpt-4o"),
        role="judge",
    )

    for cfg in (a_cfg, d_cfg, j_cfg):
        missing = [k for k, v in (("api_key", cfg.api_key), ("base_url", cfg.base_url), ("model", cfg.model)) if not v]
        if missing:
            raise ValueError(
                f"Missing {cfg.role} settings: {missing}. Set them via CLI flags or env vars "
                "(see run_majic.sh for the expected variable names)."
            )

    attacker = ChatClient(
        a_cfg,
        temperature=attacker_temperature,
        max_tokens=attacker_max_tokens,
        extract_answer=attacker_extract_answer,
    )
    defender = ChatClient(
        d_cfg,
        temperature=defender_temperature,
        max_tokens=defender_max_tokens,
    )
    judge = ChatClient(
        j_cfg,
        temperature=judge_temperature,
        max_tokens=judge_max_tokens,
    )
    return attacker, defender, judge
