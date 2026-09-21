# Extended Intro CS - Homework 5

A 2018 CS BSc Python assignment covering dense and sparse matrices, recursive determinant computation, partial functions and composition, binary-search-tree height analysis, and sequence substring matching.

## Algorithms

- Compute matrix minors and determinants for dense matrices.
- Represent sparse matrices with dictionary-backed non-zero entries and row generators.
- Compose partial functions and exponentiate them through repeated composition.
- Insert and inspect binary-search-tree nodes, including stored heights and maximum height imbalance.
- Hash fixed-length substrings and find shared sequence windows.
- Load the sequence inputs from FASTA files instead of importing very large Python string modules.

## Setup

```bash
git clone https://github.com/KobieHazon/bsc-extended-intro-cs-hw5.git
cd bsc-extended-intro-cs-hw5
uv sync --dev
```

The implementation supports Python 3.10 or newer and has no runtime dependencies.

## Usage

```bash
uv run extended-intro-hw5 det "1,2;3,4"
uv run extended-intro-hw5 intersects byebyebaboonboy babyboy 3
uv run extended-intro-hw5 genome-overlaps --max-k 150
```

The first two commands print `-2` and `bab`. The genome-overlap command uses only local FASTA files under `assignment/data/`.

## Testing

```bash
make check
```

The check target runs pytest, Ruff linting, and Ruff format validation.

## Repository Structure

- `assignment/hw5_tester.py`: supplied tester preserved in its original form
- `assignment/printree.py`: supplied tree-printing helper preserved in its original form
- `assignment/score-key.pdf`: supplied score key
- `assignment/data/`: sequence inputs stored as FASTA files
- `solution/hw5.py`: my submitted source, kept for reference
- `solution/genome_analysis.py`: my sequence-analysis script, kept for reference
- `solution/written-answers.pdf`: my exported written answers
- `hw5.py`: compatibility wrapper exposing the maintained assignment API for local tester use
- `src/`: maintained algorithms and command-line interface
- `tests/`: portable pytest regression suite, including a compatibility run of the supplied tester
