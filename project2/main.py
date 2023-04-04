import argparse
from copy import deepcopy

from CSP_Solver import CSP_Solver
from dfs import SudokuDFS
from sudoku import Version


def info(msg, pre=""):
    print(pre + '\033[94m' + "[*] " + msg + '\033[0m')

def run(ALG):
    ALL = ALG == "all"
    dfs = SudokuDFS(board=sudoku)
    if ALG == "sorted" or ALL:
        info(f"Version 'sorted' starting", pre="\n\n")
        dfs.solve(Version.SORTED)

    if ALG == "store_legal" or ALL:
        info(f"Version 'store_legal' starting", pre="\n\n")
        dfs.solve(Version.STORE_LEGAL)

    if ALG == "rec.sorted" or ALL:
        info(f"Version 'rec.sorted' starting", pre="\n\n")
        dfs.solve_recursive(sudoku, Version.SORTED)

    if ALG == "rec.store_legal" or ALL:
        info(f"Version 'rec.store_legal' starting", pre="\n\n")
        dfs.solve_recursive(sudoku, Version.STORE_LEGAL)



if __name__=="__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    algorithms = ["all", "sorted", "store_legal", "rec.sorted", "rec.store_legal"]
    parser.add_argument('--algorithm', type=str, default="all", help="The algorithms which you want to run to solve the Sudoku.", choices=algorithms)
    parser.add_argument('--n', type=int, default=3, help="This parameter controls the size of the generated board. E.g. if size is 3, the generated board is 9x9.")
    args = parser.parse_args()

    # Generate sudoku via CSP solver
    size = args.n * args.n
    info(f"Generating field of size {size}x{size}")
    solver = CSP_Solver()
    sudoku = solver.generate_unique_sudoku(args.n, 40)

    # Run CSP solver
    info(f"CSP solver starting", pre="\n\n")
    solver.solve_csp(deepcopy(sudoku), log_stats=True)

    # Run our solvers
    run(args.algorithm)