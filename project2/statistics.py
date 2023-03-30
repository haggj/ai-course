import numpy as np
from CSP_Solver import CSP_Solver
from sudoku import SudokuBoard, Version
from matplotlib import pyplot as plt
from ortools.sat.python import cp_model

import time

class Statistics:
    def __init__(self, ) -> None:
        self.solver = CSP_Solver()
        pass

    def get_perc_numbers_removed(self, sudoku_size, n):
        perc_removed_numbers = []
        std_removed_numbers = []
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

        print("Average percentage removed numbers: ", perc_removed_numbers)
        print("Standard deviation: ", std_removed_numbers)
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
    
    def compare_CSP_strategies(self, sudoku_size, n):
        start = time.time()
        avg_time = [0] * 4
        std_time = [0] * 4
        strategies = [None, cp_model.CHOOSE_FIRST, cp_model.CHOOSE_MIN_DOMAIN_SIZE, cp_model.CHOOSE_MAX_DOMAIN_SIZE]
        strategies_str = ['DEFAULT', 'CHOOSE_FIRST', 'CHOOSE_MIN_DOMAIN_SIZE', 'CHOOSE_MAX_DOMAIN_SIZE']
        strategies_int = [0, 1, 2, 3]
        solver = CSP_Solver()
        unique_sudokus = [solver.generate_random_sudoku(sudoku_size, None, remove_numbers=int(0.5*(sudoku_size**4))) for _ in range(n)]
        for i, strategy in enumerate(strategies):
            times = []
            for j in range(n):
                start = time.time()
                solver.solve_csp(unique_sudokus[j], decision_strategy=strategy)
                end = time.time()
                times.append(end - start)
            avg_time[i] = np.mean(times)
            std_time[i] = np.std(times)
        print("Average time: ", avg_time)
        print("Standard deviation: ", std_time)
        plt.figure()
        plt.plot(strategies_int, avg_time)
        plt.xlabel('Decision Strategy')
        plt.xticks(strategies_int, strategies_str)
        plt.ylabel('Average time')
        plt.title('Average time for different decision strategies')
        plt.figure()
        plt.plot(strategies_int, std_time)
        plt.xlabel('Decision Strategy')
        plt.xticks(strategies_int, strategies_str)
        plt.ylabel('Standard deviation')
        plt.title('Standard deviation of time for different decision strategies')
        plt.show()
        return
    
if __name__=="__main__":
    statistics = Statistics()
    #statistics.get_perc_numbers_removed([2,3,4], 10)
    statistics.compare_CSP_strategies(5, 100)
