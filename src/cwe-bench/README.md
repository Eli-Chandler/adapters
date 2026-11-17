# CWE-Bench adapter

## Overview

This adapter converts the public CWE-Bench v2.0.1 Harbor tasks to separate verifier mode. It reads an authorized local checkout. The agent's `/app` changes are collected as a Git patch and applied to a clean verifier container before the original verifier runs. It also adds missing benchmark author credit and omits a redundant, single-service Compose wrapper. The source revision is `d80ebe1014b49a147e77a09d67fd0a4101333ad6`.

## What is CWE-Bench?

[CWE-Bench](https://huggingface.co/datasets/collinear-ai/cwe-bench) has 100 defensive security tasks across 91 CWE types and eight languages. An agent repairs one weakness in a real codebase. A deterministic verifier checks that the weakness is closed and normal behavior still works.

## Adapter Features

- Reads the upstream task directories from `--source-dir`.
- Preserves the source task names and programmatic scoring logic. Adds cited benchmark authors where author credit is missing.
- Builds a single clean Git baseline after the source's pristine snapshot, then collects an agent patch from `/app`. The separate verifier applies that patch to its clean `/app` copy. An invalid patch scores zero; a missing patch artifact leaves the trial without a grade because transfer may have failed.
- Omits `environment/docker-compose.yaml` only when it defines the single `main` service already specified by the Dockerfile. The adapter checks the Compose and Dockerfile contents before copying.
- Supports `--limit`, `--task-ids`, and `--overwrite`.
- Checks required files and task identity before copying.
- Raises resource or build limits for eight tasks whose source limits caused Daytona oracle failures. These adjustments do not change the verifier's scoring logic.
- Keeps the random child UID/GID in `go-cwe273-35cd46d2-hardened-v3` below 65,536, within Daytona's mapped ID range. The identity check is unchanged.

## Generated Task Structure

Each generated directory contains `task.toml`, `instruction.md`, `environment/`, `tests/`, and `solution/`. All 100 tasks gain separate verifier configuration, a Git baseline in the Dockerfile, and a patch-application prelude in `tests/test.sh`. Thirty-five task configs gain an `authors` entry, and the redundant Compose file is omitted from all 100 tasks. The original verifier body and its void-on-infrastructure-failure behavior remain intact, except for the Go identity fixture range noted above.

## Run Evaluation / Harness

The source repository already has a Harbor registry entry; see the [dataset page](https://huggingface.co/datasets/collinear-ai/cwe-bench) for its run command. The adapted dataset is not registered yet. For development, run generated tasks with Harbor's oracle agent on Daytona:

```bash
harbor run -c src/cwe-bench/run_cwe-bench.yaml --ek auto_snapshot=false
```

Run all oracle trials before submitting the adapter for review. Confirm both trial status and reward for every task.

## Usage: Create Task Directories

Accept the dataset's Hugging Face access terms, then obtain a local checkout at the pinned revision. Keep this checkout outside the adapters repository.

```bash
git clone https://huggingface.co/datasets/collinear-ai/cwe-bench /path/to/cwe-bench
git -C /path/to/cwe-bench checkout d80ebe1014b49a147e77a09d67fd0a4101333ad6
cd src/cwe-bench
uv run cwe-bench --source-dir /path/to/cwe-bench --output-dir ../../datasets/cwe-bench
```

The Hugging Face checkout needs its large files, including each `environment/repo.tar.gz`. If Git LFS has not fetched them, fetch them before running the adapter.

## Comparison with Original Benchmark (Parity)

Parity experiments are pending. Separate verifier mode changes task execution and must be measured against the source tasks. The adapter contract requires oracle runs and empirical parity runs on both sides. Record the agreed agent, model, run count, raw scores, and mean ± sample SEM in `parity_experiment.json` after those runs.

Reproduce the original side with the pinned source checkout and Harbor, and the adapter side with the generated `datasets/cwe-bench` directory. Use the same agent, model, settings, and Daytona executor on both sides.

```bash
# Original side
harbor run -p /path/to/cwe-bench/tasks -a oracle -e daytona --ek auto_snapshot=false

# Adapter side
harbor run -p datasets/cwe-bench -a oracle -e daytona --ek auto_snapshot=false
```

## Notes & Caveats

The dataset is gated. Its access terms prohibit republishing solutions. Keep generated tasks local until Collinear AI and the Harbor team agree on a publication route. The adapter copies complete upstream Harbor tasks; the `task-template/` files are unused scaffold files kept for the adapter repository layout. The adapter does not change any task's network settings. The source uses `schema_version = "1.1"`, which the current Harbor task files already use; this adapter preserves it. Daytona cannot change network policy by phase when a task uses Compose mode, which is why the redundant wrapper is omitted.

Daytona oracle checks required a 2,400-second build timeout for `c-cwe326-608cfffc`; 8 GiB of memory and storage for `go-cwe295-558d2730`, `go-cwe613-75fa8fbd`, `javascript-cwe219-bedf9af6-hardened-v3`, `javascript-cwe836-0c737699-hardened-v4`, and `rust-cwe328-bd587348-hardened-v1`; and 8 GiB of memory for `java-cwe522-8914dc0a` and `typescript-cwe306-43fe6624`. The source tasks set lower limits. Each adjusted task passed a targeted Daytona oracle run with these limits.

## Installation / Prerequisites

Python 3.11 or newer, `uv`, Harbor, and access to the gated CWE-Bench dataset are required. Set up Daytona credentials for oracle and parity runs.

## Troubleshooting

- `401` from Hugging Face: accept the dataset terms and use an authorized read token.
- Missing task file: finish downloading the gated repository, including large files.
- Existing output task: pass `--overwrite` only when you intend to regenerate it.

## Citation

Gonzalez-Pumariega, Gonzalo, et al. “CWE-Bench: Refocusing Agentic Security from Exploitation to Defense.” arXiv:2610.17020 (2026). [Paper](https://arxiv.org/abs/2610.17020).

```bibtex
@misc{gonzalezpumariega2026cwebench,
  title={CWE-Bench: Refocusing Agentic Security from Exploitation to Defense},
  author={Gonzalez-Pumariega, Gonzalo and Jagannath, Ajay and Jain, Adit and Gogia, Guram and Bakshi, Soumyadeep and Rajani, Nazneen},
  year={2026},
  eprint={2610.17020},
  archivePrefix={arXiv}
}
```

## Authors & Contributions

Original benchmark: Gonzalo Gonzalez-Pumariega, Ajay Jagannath, Adit Jain, Guram Gogia, Soumyadeep Bakshi, and Nazneen Rajani. Adapter: Eli Chandler (`eli.chandler@gmail.com`).
