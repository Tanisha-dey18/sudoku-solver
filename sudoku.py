"""A Sudoku solver using backtracking with the "fewest candidates first" heuristic.

Usage:
    python sudoku.py "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    python sudoku.py --file puzzles.txt
"""

import argparse
import sys
import time

Grid = list[list[int]]


def parse(text: str) -> Grid:
    """Turns an 81-character string into a 9x9 grid. 0 or . means an empty cell."""
    chars = [ch for ch in text if ch in "0123456789."]
    if len(chars) != 81:
        raise ValueError(f"expected 81 digits, got {len(chars)}")
    values = [0 if ch == "." else int(ch) for ch in chars]
    return [values[r * 9:(r + 1) * 9] for r in range(9)]


def candidates(grid: Grid, r: int, c: int) -> set[int]:
    """Digits that can legally go in cell (r, c)."""
    used = set(grid[r])
    used.update(grid[i][c] for i in range(9))
    br, bc = 3 * (r // 3), 3 * (c // 3)
    used.update(grid[i][j] for i in range(br, br + 3) for j in range(bc, bc + 3))
    return set(range(1, 10)) - used


def is_valid(grid: Grid) -> bool:
    """True if no row, column or box repeats a filled digit."""
    groups = [grid[r] for r in range(9)]
    groups += [[grid[r][c] for r in range(9)] for c in range(9)]
    groups += [
        [grid[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)]
        for br in (0, 3, 6) for bc in (0, 3, 6)
    ]
    for group in groups:
        digits = [v for v in group if v]
        if len(digits) != len(set(digits)):
            return False
    return True


def solve(grid: Grid) -> bool:
    """Fills the grid in place. Returns False if the puzzle has no solution."""
    best = None
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                options = candidates(grid, r, c)
                # Trying the most constrained cell first prunes the search hugely
                if best is None or len(options) < len(best[2]):
                    best = (r, c, options)
                    if not options:
                        return False  # a cell with no options: dead end
    if best is None:
        return True  # no empty cells left: solved

    r, c, options = best
    for digit in options:
        grid[r][c] = digit
        if solve(grid):
            return True
    grid[r][c] = 0  # undo before backtracking
    return False


def format_grid(grid: Grid) -> str:
    lines = []
    for r in range(9):
        if r in (3, 6):
            lines.append("------+-------+------")
        row = [str(v) if v else "." for v in grid[r]]
        lines.append(" ".join(row[0:3]) + " | " + " ".join(row[3:6]) + " | " + " ".join(row[6:9]))
    return "\n".join(lines)


def run(text: str) -> int:
    try:
        grid = parse(text)
    except ValueError as err:
        print(f"Invalid puzzle: {err}", file=sys.stderr)
        return 1
    if not is_valid(grid):
        print("Invalid puzzle: a row, column or box repeats a digit.", file=sys.stderr)
        return 1

    print("Puzzle:\n" + format_grid(grid) + "\n")
    start = time.perf_counter()
    solved = solve(grid)
    elapsed_ms = (time.perf_counter() - start) * 1000
    if not solved:
        print("No solution exists.")
        return 1
    print(f"Solved in {elapsed_ms:.1f} ms:\n" + format_grid(grid) + "\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Solve Sudoku puzzles.")
    parser.add_argument("puzzle", nargs="?", help="81 characters, using 0 or . for empty cells")
    parser.add_argument("--file", help="a file with one puzzle per line (# starts a comment)")
    args = parser.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as f:
            puzzles = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        return max((run(p) for p in puzzles), default=0)
    if args.puzzle:
        return run(args.puzzle)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
