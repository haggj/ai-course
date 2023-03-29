import time
import numpy as np
from CSP_Solver import CSP_Solver
from sudoku import SudokuBoard, Version
from matplotlib import pyplot as plt

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
            print("Removed Numbers: ", removed_numbers)
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
    
if __name__=="__main__":
    statistics = Statistics()
    statistics.get_perc_numbers_removed([2,3,4], 10)
