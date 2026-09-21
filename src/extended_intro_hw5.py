"""Maintained implementations of the Homework 5 programming questions."""

from __future__ import annotations

from collections.abc import Callable, Generator, Iterable
from itertools import combinations
from numbers import Number
from pathlib import Path
from typing import Any, TypeVar

__all__ = [
    "Binary_search_tree",
    "Func",
    "Matrix",
    "SparseMatrix",
    "Tree_node",
    "analyze_genomes",
    "hash_sequence",
    "intersects",
    "load_fasta",
    "load_genomes",
    "longest_common_substring",
    "mat2a",
    "mat2b",
    "mat2c",
    "remove",
]

T = TypeVar("T")
R = TypeVar("R")

GENOME_FILES = {
    "Legionella": "legionella.fasta",
    "Brucella": "brucella.fasta",
    "Shigella": "shigella_sonnei.fasta",
    "Helicobacter": "helicobacter_pylori.fasta",
}


class Matrix:
    """Rectangular dense matrix with assignment-compatible operations."""

    def __init__(self, n: int, m: int, val: Number = 0):
        assert n > 0 and m > 0
        self.rows = [[val for _column in range(m)] for _row in range(n)]

    def dim(self) -> tuple[int, int]:
        return len(self.rows), len(self.rows[0])

    def __repr__(self) -> str:
        if len(self.rows) > 10 or len(self.rows[0]) > 10:
            return "Matrix too large, specify submatrix"
        return "".join(f"{row}\n" for row in self.rows)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Matrix) and self.rows == other.rows

    def copy(self) -> Matrix:
        n, m = self.dim()
        copied = Matrix(n, m)
        for row in range(n):
            for column in range(m):
                copied[row, column] = self[row, column]
        return copied

    def __getitem__(self, ij: tuple[int | slice, int | slice]) -> Any:
        row, column = ij
        if isinstance(row, int) and isinstance(column, int):
            return self.rows[row][column]
        if isinstance(row, slice) and isinstance(column, slice):
            sliced = Matrix(1, 1)
            sliced.rows = [source_row[column] for source_row in self.rows[row]]
            return sliced
        return NotImplemented

    def __setitem__(self, ij: tuple[int | slice, int | slice], val: Any) -> None:
        row, column = ij
        if isinstance(row, int) and isinstance(column, int):
            assert isinstance(val, Number)
            self.rows[row][column] = val
            return
        if isinstance(row, slice) and isinstance(column, slice):
            assert isinstance(val, Matrix)
            n, m = val.dim()
            target_rows = self.rows[row]
            assert len(target_rows) == n and len(target_rows[0][column]) == m
            for target_row, source_row in zip(target_rows, val.rows, strict=True):
                target_row[column] = source_row
            return
        raise TypeError("matrix indices must both be ints or both be slices")

    def entrywise_op(self, other: Matrix, op: Callable[[Number, Number], Number]) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented
        assert self.dim() == other.dim()
        n, m = self.dim()
        result = Matrix(n, m)
        for row in range(n):
            for column in range(m):
                result[row, column] = op(self[row, column], other[row, column])
        return result

    def __add__(self, other: Matrix) -> Matrix:
        return self.entrywise_op(other, lambda left, right: left + right)

    def __sub__(self, other: Matrix) -> Matrix:
        return self.entrywise_op(other, lambda left, right: left - right)

    def __neg__(self) -> Matrix:
        n, m = self.dim()
        return Matrix(n, m) - self

    def __mul__(self, other: Number) -> Matrix:
        assert isinstance(other, Number)
        n, m = self.dim()
        return self.entrywise_op(Matrix(n, m, other), lambda left, right: left * right)

    __rmul__ = __mul__

    def minor(self, i: int, j: int) -> Matrix:
        assert isinstance(i, int) and isinstance(j, int)
        n, m = self.dim()
        assert 0 <= i < n and 0 <= j < m
        result = Matrix(n - 1, m - 1)
        target_row = 0
        for source_row in range(n):
            if source_row == i:
                continue
            target_column = 0
            for source_column in range(m):
                if source_column == j:
                    continue
                result[target_row, target_column] = self[source_row, source_column]
                target_column += 1
            target_row += 1
        return result

    def det(self, i: int = 0) -> Number:
        n, m = self.dim()
        assert n == m
        assert 0 <= i < n
        if n == 1:
            return self[0, 0]
        return sum(
            ((-1) ** (i + column)) * self[i, column] * self.minor(i, column).det()
            for column in range(n)
        )


class SparseMatrix:
    """Sparse rectangular matrix storing only non-zero values."""

    def __init__(self, n: int, m: int):
        assert n > 0 and m > 0
        self.elements: dict[tuple[int, int], Number] = {}
        self.size = (n, m)

    def dim(self) -> tuple[int, int]:
        return self.size

    def __repr__(self) -> str:
        if self.size[0] > 10 or self.size[1] > 10:
            return "Matrix too large, specify submatrix"
        rows: list[str] = []
        for row in range(self.size[0]):
            values = [str(self[row, column]) for column in range(self.size[1])]
            rows.append(f"[{', '.join(values)}]")
        return "\n".join(rows) + "\n"

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, SparseMatrix)
            and self.dim() == other.dim()
            and self.elements == other.elements
        )

    def __getitem__(self, ij: tuple[int, int]) -> Number:
        row, column = ij
        assert isinstance(row, int) and isinstance(column, int)
        return self.elements.get((row, column), 0)

    def __setitem__(self, ij: tuple[int, int], val: Number) -> None:
        row, column = ij
        assert isinstance(row, int) and isinstance(column, int)
        assert isinstance(val, Number)
        assert 0 <= row < self.size[0] and 0 <= column < self.size[1]
        if val == 0:
            self.elements.pop((row, column), None)
        else:
            self.elements[(row, column)] = val

    def __add__(self, other: SparseMatrix) -> SparseMatrix:
        assert isinstance(other, SparseMatrix)
        assert self.dim() == other.dim()
        result = SparseMatrix(*self.size)
        for key, value in self.elements.items():
            result[key] = value
        for key, value in other.elements.items():
            result[key] = result[key] + value
        return result

    def __sub__(self, other: SparseMatrix) -> SparseMatrix:
        assert isinstance(other, SparseMatrix)
        assert self.dim() == other.dim()
        result = SparseMatrix(*self.size)
        for key, value in self.elements.items():
            result[key] = value
        for key, value in other.elements.items():
            result[key] = result[key] - value
        return result

    def __neg__(self) -> SparseMatrix:
        result = SparseMatrix(*self.size)
        for key, value in self.elements.items():
            result[key] = -value
        return result

    def __mul__(self, other: Number) -> SparseMatrix:
        assert isinstance(other, Number)
        result = SparseMatrix(*self.size)
        for key, value in self.elements.items():
            result[key] = value * other
        return result

    __rmul__ = __mul__

    def minor(self, i: int, j: int) -> SparseMatrix:
        assert isinstance(i, int) and isinstance(j, int)
        assert 0 <= i < self.size[0] and 0 <= j < self.size[1]
        result = SparseMatrix(self.size[0] - 1, self.size[1] - 1)
        for (row, column), value in self.elements.items():
            if row == i or column == j:
                continue
            target_row = row if row < i else row - 1
            target_column = column if column < j else column - 1
            result[target_row, target_column] = value
        return result

    def det(self, i: int = 0) -> Number:
        assert self.size[0] == self.size[1]
        assert 0 <= i < self.size[0]
        if self.size[0] == 1:
            return self[0, 0]
        return sum(
            ((-1) ** (i + column)) * self[i, column] * self.minor(i, column).det()
            for column in range(self.size[0])
        )

    def gen_row1(self, i: int) -> Generator[Number]:
        assert 0 <= i < self.size[0]
        for column in range(self.size[1]):
            value = self[i, column]
            if value != 0:
                yield value

    def gen_row2(self, i: int) -> Generator[Number]:
        assert 0 <= i < self.size[0]
        for (row, _column), value in self.elements.items():
            if row == i:
                yield value


def mat2a() -> None:
    return None


def mat2b() -> SparseMatrix:
    matrix = SparseMatrix(3, 3)
    matrix[2, 0] = 1
    matrix[2, 1] = 6
    return matrix


def mat2c() -> SparseMatrix:
    matrix = SparseMatrix(3, 3)
    matrix[2, 2] = 2
    matrix[2, 1] = 1
    return matrix


class Func:
    """Partial function with assignment-compatible composition helpers."""

    def __init__(self, func: Callable[[T], R], domain: Callable[[T], bool]):
        self.func = func
        self.domain = domain

    def __call__(self, x: T) -> R | None:
        try:
            if self.domain(x):
                return self.func(x)
        except Exception:
            return None
        return None

    def compose(self, other: Func) -> Func:
        def domain(x: Any) -> bool:
            intermediate = other(x)
            return intermediate is not None and self.domain(intermediate)

        def func(x: Any) -> Any:
            intermediate = other(x)
            if intermediate is None:
                return None
            return self(intermediate)

        return Func(func, domain)

    def exp(self, k: int) -> Func:
        assert k >= 1
        result = self
        for _ in range(k - 1):
            result = self.compose(result)
        return result

    def exp_rec(self, k: int) -> Func:
        assert k >= 1
        if k == 1:
            return self
        return self.compose(self.exp_rec(k - 1))


class Tree_node:
    """Node used by the assignment binary search tree."""

    def __init__(self, key: Any, val: Any):
        self.key = key
        self.val = val
        self.left: Tree_node | None = None
        self.right: Tree_node | None = None
        self.height = 0

    def __repr__(self) -> str:
        return f"({self.key}:{self.val})"


class Binary_search_tree:
    """Unbalanced binary search tree with assignment operations."""

    def __init__(self):
        self.root: Tree_node | None = None

    def __repr__(self) -> str:
        def rows(node: Tree_node | None, depth: int = 0) -> list[str]:
            if node is None:
                return []
            return (
                rows(node.right, depth + 1)
                + ["    " * depth + repr(node)]
                + rows(node.left, depth + 1)
            )

        return "\n".join(rows(self.root)) + ("\n" if self.root is not None else "")

    def lookup(self, key: Any) -> Tree_node | None:
        node = self.root
        while node is not None:
            if key == node.key:
                return node
            node = node.left if key < node.key else node.right
        return None

    def insert(self, key: Any, val: Any) -> None:
        if self.root is None:
            self.root = Tree_node(key, val)
            return
        node = self.root
        while True:
            if key == node.key:
                node.val = val
                return
            if key < node.key:
                if node.left is None:
                    node.left = Tree_node(key, val)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = Tree_node(key, val)
                    return
                node = node.right

    def minimum(self) -> Tree_node | None:
        node = self.root
        if node is None:
            return None
        while node.left is not None:
            node = node.left
        return node

    def depth(self) -> int:
        def depth_rec(node: Tree_node | None) -> int:
            if node is None:
                return -1
            return 1 + max(depth_rec(node.left), depth_rec(node.right))

        return depth_rec(self.root)

    def size(self) -> int:
        def size_rec(node: Tree_node | None) -> int:
            if node is None:
                return 0
            return 1 + size_rec(node.left) + size_rec(node.right)

        return size_rec(self.root)

    def store_heights(self) -> None:
        def store_heights_rec(node: Tree_node | None) -> int:
            if node is None:
                return -1
            node.height = 1 + max(store_heights_rec(node.left), store_heights_rec(node.right))
            return node.height

        store_heights_rec(self.root)

    def height_diff(self) -> int:
        self.store_heights()

        def height_diff_rec(node: Tree_node | None) -> int:
            if node is None:
                return 0
            left_height = node.left.height if node.left is not None else -1
            right_height = node.right.height if node.right is not None else -1
            return max(
                abs(left_height - right_height),
                height_diff_rec(node.left),
                height_diff_rec(node.right),
            )

        return height_diff_rec(self.root)


def remove(string: str, char: str) -> str:
    return "".join(letter for letter in string if letter != char)


def hash_sequence(genome: str, k: int) -> dict[str, list[int]]:
    if k < 1:
        raise ValueError("k must be positive")
    result: dict[str, list[int]] = {}
    for index in range(len(genome) - k + 1):
        result.setdefault(genome[index : index + k], []).append(index)
    return result


def intersects(genome1: str, genome2: str, k: int) -> str | None:
    if k < 1:
        raise ValueError("k must be positive")
    if k > min(len(genome1), len(genome2)):
        return None
    shorter, longer = (genome1, genome2) if len(genome1) < len(genome2) else (genome2, genome1)
    candidates = hash_sequence(shorter, k)
    for index in range(len(longer) - k + 1):
        substring = longer[index : index + k]
        if substring in candidates:
            return substring
    return None


def longest_common_substring(
    genome1: str, genome2: str, max_k: int | None = None
) -> tuple[int, str]:
    high = min(len(genome1), len(genome2))
    if max_k is not None:
        high = min(high, max_k)
    low = 0
    found = ""
    while low < high:
        midpoint = (low + high + 1) // 2
        candidate = intersects(genome1, genome2, midpoint)
        if candidate is None:
            high = midpoint - 1
        else:
            low = midpoint
            found = candidate
    if low and len(found) != low:
        found = intersects(genome1, genome2, low) or ""
    return low, found


def load_fasta(path: Path) -> str:
    sequence: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(">"):
            continue
        sequence.append(stripped.upper())
    return "".join(sequence)


def load_genomes(data_dir: Path) -> dict[str, str]:
    return {name: load_fasta(data_dir / filename) for name, filename in GENOME_FILES.items()}


def analyze_genomes(
    data_dir: Path, max_k: int = 150
) -> Iterable[tuple[tuple[str, str], tuple[int, str]]]:
    genomes = load_genomes(data_dir)
    for left, right in combinations(genomes, 2):
        yield (left, right), longest_common_substring(genomes[left], genomes[right], max_k=max_k)
