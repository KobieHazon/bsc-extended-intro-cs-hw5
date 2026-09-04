from pathlib import Path

import pytest

from extended_intro_hw5 import (
    Binary_search_tree,
    Func,
    Matrix,
    SparseMatrix,
    hash_sequence,
    intersects,
    load_genomes,
    mat2a,
    mat2b,
    mat2c,
)

IUPAC_DNA = set("ACGTRYSWKMBDHVN")


def test_dense_matrix_minor_and_determinant():
    matrix = Matrix(3, 3)
    for row, values in enumerate(([1, 2, 3], [4, 5, 6], [7, 600, 9])):
        for column, value in enumerate(values):
            matrix[row, column] = value

    assert matrix.minor(1, 2).rows == [[1, 2], [7, 600]]
    assert matrix.det() == 3552


def test_sparse_matrix_arithmetic_minor_and_generators():
    matrix = SparseMatrix(3, 4)
    matrix[1, 0] = 3
    matrix[1, 1] = -10
    matrix[2, 3] = 90

    assert sorted(matrix.gen_row1(1)) == [-10, 3]
    assert sorted(matrix.gen_row2(1)) == [-10, 3]
    assert list(matrix.gen_row2(0)) == []
    assert (-matrix)[1, 0] == -3
    assert (3 * matrix)[2, 3] == 270

    square = SparseMatrix(3, 3)
    for row, values in enumerate(([1, 2, 3], [4, 5, 6], [7, 600, 9])):
        for column, value in enumerate(values):
            square[row, column] = value
    assert square.minor(0, 0).elements == {(0, 0): 5, (0, 1): 6, (1, 0): 600, (1, 1): 9}
    assert square.det() == 3552


def test_assignment_matrix_answers():
    assert mat2a() is None
    assert mat2b().elements == {(2, 0): 1, (2, 1): 6}
    assert mat2c().elements == {(2, 1): 1, (2, 2): 2}


def test_partial_function_composition_and_exponentiation():
    square = Func(lambda x: x**2, lambda _x: True)
    rational = Func(lambda x: (5 * x) / (x - 9), lambda x: x != 9)

    assert rational.compose(square)(3) is None
    assert square.compose(rational)(3) == 6.25
    assert square.compose(square)(7) == 2401
    assert square.exp(7)(2) == 340282366920938463463374607431768211456
    assert rational.exp(10)(81 / 4) is None
    assert rational.exp_rec(10)(81 / 4) is None


def test_binary_search_tree_height_metrics():
    tree = Binary_search_tree()
    for key, value in [(10, "a"), (6, "a"), (14, "a"), (1, "a"), (3, "a"), (20, "a"), (7, "a")]:
        tree.insert(key, value)

    assert tree.size() == 7
    assert tree.minimum().key == 1
    tree.store_heights()
    assert tree.lookup(6).height == 2
    assert tree.height_diff() == 1

    skewed = Binary_search_tree()
    for key in range(10):
        skewed.insert(key, "x")
    assert skewed.height_diff() == 9


def test_sequence_hashing_and_intersection():
    assert hash_sequence("byebyeboy", 3) == {
        "bye": [0, 3],
        "yeb": [1, 4],
        "eby": [2],
        "ebo": [5],
        "boy": [6],
    }
    assert intersects("abcdefg", "gfedabc", 4) is None
    assert intersects("abcdefg", "gfedabc", 3) == "abc"
    assert intersects("blablablablabla", "blablablablabla", 15) == "blablablablabla"
    with pytest.raises(ValueError):
        hash_sequence("abc", 0)


def test_local_fasta_inputs_load_without_external_services():
    data_dir = Path(__file__).resolve().parents[1] / "assignment" / "data"
    genomes = load_genomes(data_dir)

    assert set(genomes) == {"Legionella", "Brucella", "Shigella", "Helicobacter"}
    assert all(len(sequence) > 1_000_000 for sequence in genomes.values())
    assert all(set(sequence) <= IUPAC_DNA for sequence in genomes.values())
