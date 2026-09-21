"""Repository-level checks for publication preparation."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TEXT_SKIP_SUFFIXES = {
    ".bmp",
    ".gif",
    ".ico",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".pyc",
    ".zip",
}
FORBIDDEN_PATTERNS = [
    re.compile(bytes.fromhex("323038323334313631")),
    re.compile(b"/" + b"Users/"),
    re.compile(b"/home/" + b"kobie"),
    re.compile(b"/home/" + b"arkadiros"),
    re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
]
IUPAC_DNA = set("ACGTRYSWKMBDHVN")


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )
    return [REPO_ROOT / item.decode() for item in result.stdout.split(b"\0") if item]


def check_privacy(files: list[Path]) -> None:
    failures: list[str] = []
    for path in files:
        if path.suffix.lower() in TEXT_SKIP_SUFFIXES:
            continue
        data = path.read_bytes()
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(data):
                failures.append(str(path.relative_to(REPO_ROOT)))
                break
    if failures:
        joined = ", ".join(sorted(failures))
        raise SystemExit(f"privacy markers found in tracked files: {joined}")


def check_fasta_files() -> None:
    data_dir = REPO_ROOT / "assignment" / "data"
    expected = {
        "brucella.fasta",
        "helicobacter_pylori.fasta",
        "legionella.fasta",
        "shigella_sonnei.fasta",
    }
    actual = {path.name for path in data_dir.glob("*.fasta")}
    if actual != expected:
        raise SystemExit(f"unexpected FASTA set: {sorted(actual)}")
    for path in sorted(data_dir.glob("*.fasta")):
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines or not lines[0].startswith(">") or lines[0].startswith(">>"):
            raise SystemExit(f"invalid FASTA header in {path.relative_to(REPO_ROOT)}")
        sequence = "".join(line.strip().upper() for line in lines[1:] if line.strip())
        if not sequence:
            raise SystemExit(f"empty FASTA sequence in {path.relative_to(REPO_ROOT)}")
        invalid = sorted(set(sequence) - IUPAC_DNA)
        if invalid:
            raise SystemExit(f"invalid FASTA symbols in {path.relative_to(REPO_ROOT)}: {invalid}")


def check_current_tree() -> None:
    forbidden_paths = {
        "Brucella.py",
        "Helicobacter_pylori.py",
        "Legionella.py",
        "Shigella_sonnei.py",
        "genome_analysis.py",
    }
    current = {path.relative_to(REPO_ROOT).as_posix() for path in tracked_files()}
    if forbidden_paths & current:
        raise SystemExit(
            f"legacy large module files still tracked: {sorted(forbidden_paths & current)}"
        )
    required = {
        "README.md",
        "hw5.py",
        "src/extended_intro_hw5.py",
        "tests/test_exercises.py",
        "solution/hw5.py",
        "solution/genome_analysis.py",
    }
    missing = sorted(required - current)
    if missing:
        raise SystemExit(f"required files missing from tracked tree: {missing}")


def main() -> None:
    files = tracked_files()
    check_privacy(files)
    check_fasta_files()
    check_current_tree()
    print("repository check passed")


if __name__ == "__main__":
    main()
