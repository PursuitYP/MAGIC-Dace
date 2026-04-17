"""Read and inspect parquet file contents."""

import argparse
import json
import pandas as pd


def pretty_print_row(idx, row):
    """Print a single row in a readable format."""
    print(f"--- Row {idx} ---")
    for col, val in row.items():
        val_str = str(val)
        # For list/dict-like fields, try to pretty-print
        if col == "prompt":
            try:
                parsed = json.loads(val_str) if isinstance(val, str) else val
                if isinstance(parsed, list):
                    # Show role and truncated content for chat messages
                    for msg in parsed:
                        role = msg.get("role", "?")
                        content = msg.get("content", "")
                        if len(content) > 200:
                            content = content[:200] + "..."
                        print(f"  {col} [{role}]: {content}")
                    continue
            except (json.JSONDecodeError, TypeError):
                pass
        # Truncate long values
        # if len(val_str) > 200:
        #     val_str = val_str[:200] + "..."
        print(f"  {col}: {val_str}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Read and display parquet file contents")
    parser.add_argument("file", help="Path to the parquet file")
    parser.add_argument("-n", "--nrows", type=int, default=3, help="Number of rows to show from head/tail (default: 3)")
    parser.add_argument("--columns", nargs="*", help="Specific columns to display")
    parser.add_argument("--full", action="store_true", help="Show full content without truncation")
    args = parser.parse_args()

    df = pd.read_parquet(args.file)

    if args.columns:
        df = df[[c for c in args.columns if c in df.columns]]

    print(f"File: {args.file}")
    print(f"Total: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")
    print()

    print(f"=== First {args.nrows} rows ===")
    print()
    for i in range(min(args.nrows, len(df))):
        pretty_print_row(i, df.iloc[i])

    print(f"=== Last {args.nrows} rows ===")
    print()
    start = max(len(df) - args.nrows, 0)
    for i in range(start, len(df)):
        pretty_print_row(i, df.iloc[i])


if __name__ == "__main__":
    main()


# 主要改动：

# - 默认显示前 3 行和后 3 行（-n 3）                                                                                                                                                                                        
# - 先打印文件总数据量，再逐行格式化输出每条记录
# - prompt 字段按 chat message 格式展示（role + 截断的 content）                                                                                                                                                            
# - 长字段自动截断到 200 字符，加 ...                                                                                                                                                                                     
# - 每行用 --- Row N --- 分隔，更清晰                                                                                                                                                                                     

# python data/safety/read_parquet.py data/safety/train_dace.parquet