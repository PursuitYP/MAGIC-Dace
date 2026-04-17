### dace: count unique vanilla entries in harmful and benign sft jsonl outputs ###
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILES = [
    "sft_data_source_harmful.jsonl",
    "sft_data_source_benign.jsonl",
]


def count_unique_vanilla(path):
    total = 0
    seen = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            vanilla = item.get("vanilla")
            if vanilla is None:
                continue
            total += 1
            seen.add(vanilla)
    return total, len(seen)


def main():
    for filename in FILES:
        path = os.path.join(BASE_DIR, filename)
        total, unique = count_unique_vanilla(path)
        duplicates = total - unique
        print(f"{filename}: total={total}, unique={unique}, duplicates={duplicates}")


if __name__ == "__main__":
    main()


# cd /mnt/shared-storage-user/yupeng/MAGIC/data-sft && python count_unique_vanilla.py
