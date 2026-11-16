"""Generate CWE-Bench tasks from an authorized upstream checkout."""

import argparse
from pathlib import Path

from .adapter import CWEBenchAdapter


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("datasets/cwe-bench"))
    parser.add_argument("--limit", type=int)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--task-ids", nargs="+")
    args = parser.parse_args()

    generated = CWEBenchAdapter(
        args.output_dir,
        args.source_dir,
        limit=args.limit,
        overwrite=args.overwrite,
        task_ids=args.task_ids,
    ).run()
    print(f"Copied {len(generated)} CWE-Bench tasks to {args.output_dir}")


if __name__ == "__main__":
    main()
