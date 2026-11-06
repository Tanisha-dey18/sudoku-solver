"""Run with: python -m unittest"""

import unittest

from sudoku import candidates, is_valid, parse, solve

EASY = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
EASY_SOLUTION = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"
HARD = "1....7.9..3..2...8..96..5....53..9...1..8...26....4...3......1..4......7..7...3.."


def flatten(grid):
    return "".join(str(v) for row in grid for v in row)


class TestSudoku(unittest.TestCase):
    def test_parse_accepts_dots_and_zeros(self):
        self.assertEqual(parse("." * 81), parse("0" * 81))

    def test_parse_rejects_wrong_length(self):
        with self.assertRaises(ValueError):
            parse("123")

    def test_candidates(self):
        grid = parse(EASY)
        # Row 0 has 5,3,7; column 2 has 8; box 0 has 5,3,6,9,8
        self.assertEqual(candidates(grid, 0, 2), {1, 2, 4})

    def test_detects_duplicate_in_row(self):
        self.assertFalse(is_valid(parse("11" + "0" * 79)))

    def test_solves_easy_puzzle(self):
        grid = parse(EASY)
        self.assertTrue(solve(grid))
        self.assertEqual(flatten(grid), EASY_SOLUTION)

    def test_solves_hard_puzzle_validly(self):
        original = parse(HARD)
        grid = parse(HARD)
        self.assertTrue(solve(grid))
        self.assertTrue(is_valid(grid))
        self.assertTrue(all(all(row) for row in grid))
        # Every given clue is kept
        for r in range(9):
            for c in range(9):
                if original[r][c]:
                    self.assertEqual(grid[r][c], original[r][c])

    def test_unsolvable_puzzle(self):
        # Valid so far, but cell (0, 8) cannot take any digit: 1-8 in its row, 9 in its column
        grid = parse("123456780" + "000000009" + "0" * 63)
        self.assertTrue(is_valid(grid))
        self.assertFalse(solve(grid))


if __name__ == "__main__":
    unittest.main()
