"""Generate CWE-Bench tasks from an authorized upstream checkout."""

import argparse
from pathlib import Path

from .adapter import CWEBenchAdapter


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate CWE-Bench tasks with separate verifiers.")
    parser.add_argument("--source-dir", type=Path, required=True, help="Root of the upstream dataset checkout")
    parser.add_argument(
        "--output-dir", type=Path, default=Path("datasets/cwe-bench"), help="Output directory (default: %(default)s)"
    )
    parser.add_argument("--limit", type=int, help="Maximum number of tasks to generate")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing generated task directories")
    parser.add_argument("--task-ids", nargs="+", help="Generate only the specified upstream task directories")
    args = parser.parse_args()

    generated = CWEBenchAdapter(
        args.output_dir,
        args.source_dir,
        limit=args.limit,
        overwrite=args.overwrite,
        task_ids=args.task_ids,
    ).run()
    print(f"Generated {len(generated)} CWE-Bench tasks in {args.output_dir}")


if __name__ == "__main__":
    main()
