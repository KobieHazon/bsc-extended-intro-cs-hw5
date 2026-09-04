"""Command-line interface for the maintained Homework 5 implementation."""

from __future__ import annotations

import argparse
from pathlib import Path

from extended_intro_hw5.exercises import Matrix, analyze_genomes, intersects


def parse_matrix(raw: str) -> Matrix:
    rows = [[int(value.strip()) for value in row.split(",")] for row in raw.split(";")]
    if not rows or not rows[0]:
        raise argparse.ArgumentTypeError("matrix must contain at least one value")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise argparse.ArgumentTypeError("all matrix rows must have the same width")
    matrix = Matrix(len(rows), width)
    for row_index, row in enumerate(rows):
        for column_index, value in enumerate(row):
            matrix[row_index, column_index] = value
    return matrix


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="extended-intro-hw5")
    subparsers = parser.add_subparsers(dest="command", required=True)

    det_parser = subparsers.add_parser("det", help="compute a matrix determinant")
    det_parser.add_argument("matrix", type=parse_matrix, help='rows such as "1,2;3,4"')

    intersects_parser = subparsers.add_parser("intersects", help="find a shared substring")
    intersects_parser.add_argument("left")
    intersects_parser.add_argument("right")
    intersects_parser.add_argument("length", type=int)

    genome_parser = subparsers.add_parser("genome-overlaps", help="compare local FASTA inputs")
    genome_parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("assignment/data"),
        help="directory containing the recovered FASTA files",
    )
    genome_parser.add_argument(
        "--max-k",
        type=int,
        default=150,
        help="maximum substring length to check",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "det":
        print(args.matrix.det())
    elif args.command == "intersects":
        print(intersects(args.left, args.right, args.length))
    elif args.command == "genome-overlaps":
        for (left, right), (length, substring) in analyze_genomes(args.data_dir, max_k=args.max_k):
            print(f"{left} / {right}: {length} {substring}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
