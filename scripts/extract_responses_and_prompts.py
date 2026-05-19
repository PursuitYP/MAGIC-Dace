### dace: extract attacker rewrites into unified {rewrite_prompt} jsonl files ###
"""
Output (next to this script):
  - scripts/dace_history.jsonl       (from DACE-Diversity ... w_dace_sft_full replay_buffer, steps 270-284)
  - scripts/magic_history.jsonl      (from D-q257bi-A-q257bisft ... replay_buffer, steps 270-284)
  - scripts/dace_replay_pool.jsonl   (from DACE-Diversity ... w_dace_sft_v4 global_step_300/archive_pool.json)

Each line has exactly one field: {"rewrite_prompt": "..."}.

  - For the two replay_buffer sources, each jsonl line in a step file holds 4 GRPO
    rollouts under `response`; we unroll them into 4 rewrite_prompt entries.
    15 steps * 64 questions * 4 = 3840 lines per file.
  - For the archive_pool, each entry's `prompt_text` becomes one rewrite_prompt.
    Total = pool size (4000).
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

REPLAY_SOURCES = [
    (
        "dace_history",
        "/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/yupeng/ckpt/Game-separated/"
        "DACE-Diversity-Qwen2.5_7B_Instruct-w_dace_sft_full-2026-04-26_22-00-31/replay_buffer",
    ),
    (
        "magic_history",
        "/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/yupeng/ckpt/Game-separated/"
        "D-q257bi-A-q257bisft_wocode-reward1_0.5_0-woDformat-wo_label_reward-revised_label-tp2-"
        "2026-03-31_12-55-34/replay_buffer",
    ),
]

ARCHIVE_POOL_PATH = (
    "/mnt/shared-storage-gpfs2/wenxiaoyu-gpfs02/yupeng/ckpt/Game-separated/"
    "DACE-Diversity-Qwen2.5_7B_Instruct-w_dace_sft_v4-2026-05-03_14-30-23/"
    "global_step_300/archive_pool.json"
)

STEP_START = 270
STEP_END = 284  # inclusive
GRPO_GROUP = 4


def extract_replay(tag: str, replay_dir: str, out_path: str) -> int:
    n = 0
    with open(out_path, "w", encoding="utf-8") as fout:
        for step in range(STEP_START, STEP_END + 1):
            fpath = os.path.join(replay_dir, f"train_step_{step}.jsonl")
            if not os.path.isfile(fpath):
                raise FileNotFoundError(f"missing replay step file: {fpath}")
            with open(fpath, "r", encoding="utf-8") as fin:
                for line in fin:
                    line = line.strip()
                    if not line:
                        continue
                    rec = json.loads(line)
                    responses = rec.get("response", [])
                    if not isinstance(responses, list):
                        raise ValueError(f"response not list in {fpath}")
                    if len(responses) != GRPO_GROUP:
                        print(f"[warn] {fpath}: got {len(responses)} responses, expected {GRPO_GROUP}")
                    for r in responses:
                        fout.write(json.dumps({"rewrite_prompt": r}, ensure_ascii=False) + "\n")
                        n += 1
    print(f"[{tag}] wrote {n} lines -> {out_path}")
    return n


def extract_archive_pool(pool_path: str, out_path: str) -> int:
    with open(pool_path, "r", encoding="utf-8") as f:
        pool = json.load(f)
    entries = pool.get("entries", [])
    n = 0
    with open(out_path, "w", encoding="utf-8") as fout:
        for e in entries:
            fout.write(
                json.dumps({"rewrite_prompt": e.get("prompt_text")}, ensure_ascii=False) + "\n"
            )
            n += 1
    print(f"[dace_replay_pool] wrote {n} lines -> {out_path}")
    return n


def main():
    expected_per_folder = (STEP_END - STEP_START + 1) * 64 * GRPO_GROUP  # 3840
    for tag, rdir in REPLAY_SOURCES:
        out = os.path.join(SCRIPT_DIR, f"{tag}.jsonl")
        n = extract_replay(tag, rdir, out)
        if n != expected_per_folder:
            print(f"[warn] {tag}: got {n}, expected {expected_per_folder}")

    out_pool = os.path.join(SCRIPT_DIR, "dace_replay_pool.jsonl")
    extract_archive_pool(ARCHIVE_POOL_PATH, out_pool)


if __name__ == "__main__":
    main()
