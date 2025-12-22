# THE FUNCTION WHICH SOLVES ALL THE SUDOKU PROBLEMS
# IN THE INPUT FILE USING BACKTRACKING AND WRITES THE OUTPUT TO THE OUTPUT FILE

from search import *
from time import perf_counter
import time
import argparse

#THE MAIN FUNCTION GOES HERE
if __name__ == "__main__":
    """Runner for Sudoku solver.

    Usage example:
      python sudoku.py --inputFile data/euler.txt --outputFile output.txt

    Notes:
      - Input file should contain one puzzle per line (81 chars). Use '0' or '.' for empty cells.
      - The solver (Backtracking_Search) should return either a dict mapping each square to a
        single-digit string on success, or the string "FAILURE" on failure.
    """
    argument_parser = argparse.ArgumentParser(description="Sudoku Solving Problem")
    argument_parser.add_argument("--inputFile", type=str, required=True, help="Sudoku Input File")
    argument_parser.add_argument("--outputFile", type=str, default="output.txt", help="Output file to write solutions")
    args = argument_parser.parse_args()

    filename = args.inputFile
    output_file = args.outputFile

    puzzles = []
    with open(filename, "r") as ins:
        for line in ins:
            grid = line.strip()
            if not grid:
                continue
            puzzles.append(grid)

    solved_count = 0
    boardno = 0
    start = perf_counter()

    with open(output_file, "w") as f:
        for grid in puzzles:
            boardno += 1
            start_puzzle = perf_counter()
            try:
                sudoku = csp(grid=grid)
                solved = Backtracking_Search(sudoku)
            except Exception as e:
                # Log the error and continue with next puzzle
                print(f"Error while solving board {boardno}: {e}")
                continue

            elapsed = perf_counter() - start_puzzle
            print(f"The board - {boardno} takes {elapsed:.4f} seconds")
            if solved != "FAILURE":
                print("After solving:")
                display(solved)
                f.write(write(solved) + "\n")
                solved_count += 1

    total_time = perf_counter() - start
    print(f"Number of problems solved is: {solved_count}")
    print(f"Time taken to solve the puzzles is: {total_time:.4f} seconds")