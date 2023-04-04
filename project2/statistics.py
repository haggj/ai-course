import numpy as np
from CSP_Solver import CSP_Solver
from dfs import SudokuDFS
from sudoku import SudokuBoard, Version
from matplotlib import pyplot as plt
from ortools.sat.python import cp_model
from copy import deepcopy
import time

class Statistics:
    def __init__(self, ) -> None:
        self.solver = CSP_Solver()
        pass

    def get_perc_numbers_removed(self, sudoku_size, n):
        perc_removed_numbers = []
        std_removed_numbers = []

        # Run n experiments for different sudoku sizes and record statistics
        for size in sudoku_size:
            avg_removed_numbers = 0
            removed_numbers = []
            for i in range(0, n):
                sb, rn = self.solver.generate_unique_sudoku(size, None, True)
                print("Removed Numbers: ", rn)
                removed_numbers.append(rn)
            avg_removed_numbers = np.mean(removed_numbers)
            perc_removed_numbers.append(avg_removed_numbers/(size**4)*100)
            std_removed_numbers.append(np.std(removed_numbers))

        # Plot results
        print("Percentage of removed numbers: ", perc_removed_numbers)
        plt.figure()
        plt.plot(sudoku_size, perc_removed_numbers)
        plt.xlabel('Sudoku Size')
        plt.xticks(sudoku_size, [str(size**2) + 'x' + str(size**2) for size in sudoku_size])
        plt.ylabel('Percentage of removed numbers')
        plt.title('Percentage of removed numbers for different Sudoku sizes')
        plt.figure()
        plt.plot(sudoku_size, std_removed_numbers)
        plt.xlabel('Sudoku Size')
        plt.xticks(sudoku_size, [str(size**2) + 'x' + str(size**2) for size in sudoku_size])
        plt.ylabel('Standard deviation')
        plt.title('Standard deviation of removed numbers for different Sudoku sizes')
        plt.show()
        return
    
    def compare_strategies(self, sudoku_size, n):
        avg_time = []
        std_time = []

        # Run n experiments for different sudoku sizes and record statistics
        for size in sudoku_size:
            times = [[] for i in range(5)]
            for i in range(n):
                solver = CSP_Solver()
                sudoku = solver.generate_unique_sudoku(size, 40)
                start = time.time()
                solver.solve_csp(sudoku, decision_strategy=None)
                end = time.time()
                times[0].append(end-start)
                dfs = SudokuDFS(board=sudoku)
                sol1 = dfs.solve(Version.SORTED)
                times[4].append(dfs.duration)
                sol2 = dfs.solve(Version.STORE_LEGAL)
                times[2].append(dfs.duration)
                sol3 = dfs.solve_recursive(sudoku, Version.SORTED)
                times[3].append(dfs.duration)
                sol4 = dfs.solve_recursive(sudoku, Version.STORE_LEGAL)
                times[1].append(dfs.duration)
            avg_time.append([np.mean(t) for t in times])
            std_time.append([np.std(t) for t in times])
        
        # Plot results
        print("Average time: ", avg_time)
        plt.figure()
        for size in range(len(sudoku_size)):
            plt.plot([0, 1, 2, 3, 4], avg_time[size], label=str(sudoku_size[size]**2) + 'x' + str(sudoku_size[size]**2))
        plt.xlabel('Decision Strategy')
        plt.xticks([0, 1, 2, 3, 4], ['CSP', 'DFS_STORE_LEGAL_RECURSIVE', 'DFS_STORE_LEGAL', 'DFS_SORTED_RECURSIVE', 'DFS_SORTED'])
        plt.ylabel('Average time [s]')
        plt.title('Average time for different decision strategies')
        plt.legend()
        plt.figure()
        for size in range(len(sudoku_size)):
            plt.plot([0, 1, 2, 3, 4], std_time[size], label=str(sudoku_size[size]**2) + 'x' + str(sudoku_size[size]**2))
        plt.xlabel('Decision Strategy')
        plt.xticks([0, 1, 2, 3, 4], ['CSP', 'DFS_STORE_LEGAL_RECURSIVE', 'DFS_STORE_LEGAL', 'DFS_SORTED_RECURSIVE', 'DFS_SORTED'])
        plt.ylabel('Standard deviation')
        plt.title('Standard deviation of time for different decision strategies')
        plt.legend()
        plt.show()
        return
    
if __name__=="__main__":
    statistics = Statistics()
    #statistics.get_perc_numbers_removed([2,3,4], 10)
    statistics.compare_strategies([3,4], 10)