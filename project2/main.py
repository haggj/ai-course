import argparse
from copy import deepcopy

from CSP_Solver import CSP_Solver
from dfs import SudokuDFS
from sudoku import Version
from statistics import Statistics


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

def plot(args):
    statistics = Statistics()
    if isinstance(args.n, int):
        info(f"Input more than one sudoku size to plot, e.g. --n 2 3 4", pre="\n\n")
        return
    if args.plot_comparison:
        info(f"Compare strategies starting for sudoku sizes {args.n}", pre="\n\n")
        statistics.compare_strategies(args.n, args.s)
    if args.plot_numbers_removed:
        info(f"Get percentage of removed numbers starting for sudoku sizes {args.n}", pre="\n\n")
        statistics.get_perc_numbers_removed(args.n, args.s)

if __name__=="__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    algorithms = ["all", "sorted", "store_legal", "rec.sorted", "rec.store_legal"]
    parser.add_argument('--algorithm', type=str, default="all", help="The algorithms which you want to run to solve the Sudoku.", choices=algorithms)
    parser.add_argument('--n', type=int, nargs="+", default=3, help="This parameter controls the size of the generated board. E.g. if size is 3, the generated board is 9x9.")
    parser.add_argument('--plot_comparison', type=bool, default=False, help="With this parameter the required time of different DFS strategies and the CSP solver can be plotted.")
    parser.add_argument('--plot_numbers_removed', type=bool, default=False, help="With this parameter the percentage of numbers removed until the sudoku no longer has only one solution can be plotted.")
    parser.add_argument('--s', type=int, default=10, help="This parameter controls the number of experiments which are run to plot the statistics.")
    args = parser.parse_args()

    # Plot statistics
    if args.plot_comparison or args.plot_numbers_removed:
        plot(args)
        exit()

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