# 🔢 Sudoku Solver

A small command-line Sudoku solver in plain Python. It uses **backtracking** with the **"fewest candidates first"** heuristic. No dependencies.

## Usage

Requires Python 3.9+.

Solve one puzzle (81 characters, `0` or `.` for empty cells):

```bash
python sudoku.py "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
```

```
Solved in 5.3 ms:
5 3 4 | 6 7 8 | 9 1 2
6 7 2 | 1 9 5 | 3 4 8
1 9 8 | 3 4 2 | 5 6 7
------+-------+------
...
```

Solve every puzzle in a file (one per line, `#` for comments):

```bash
python sudoku.py --file puzzles.txt
```

Invalid input (wrong length, or a repeated digit in a row, column or box) is reported with exit code `1`. Timings depend on your machine.

## How it works

1. **Find the most constrained empty cell.** For each empty cell, compute its *candidates*: digits 1–9 not already in its row, column or 3×3 box. Pick the cell with the fewest.
2. **Dead end?** If some empty cell has zero candidates, this branch is impossible, so return `False` immediately.
3. **Try each candidate** in that cell and recurse.
4. **Backtrack.** If no candidate leads to a solution, clear the cell and return `False` so the caller tries its next option.

Picking the most constrained cell first matters. Cells with only one candidate get filled without any guessing, and wrong guesses are detected very early. Plain left-to-right backtracking can take thousands of times longer on hard puzzles.

## Project structure

| File              | Purpose                                     |
|-------------------|---------------------------------------------|
| `sudoku.py`       | Parser, validator, solver and CLI           |
| `test_sudoku.py`  | Unit tests                                  |
| `puzzles.txt`     | Sample puzzles: an easy one and "AI Escargot" |

## Run the tests

```bash
python -m unittest -v
```

## License

[MIT](LICENSE)
