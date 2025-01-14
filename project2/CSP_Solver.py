import copy

from sudoku import SudokuBoard
from ortools.sat.python import cp_model

import time

EMPTY_SPACE = 0

# CSP Callback function executed on each found Solution
class VarArraySolutionCounter(cp_model.CpSolverSolutionCallback):
    """Count intermediate solutions."""

    def __init__(self):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        #print("Solution #", str(self.__solution_count))

    def solution_count(self):
        return self.__solution_count

class CSP_Solver:
    def __init__(self, board=SudokuBoard(3)):
        # initialize Board
        self.board = board._board
        self.board_size = board.size
        self.board_size_sqrt = board.size_sqrt
        self.variables = []
        self.solver_variables = []
        # csp env
        self.model = cp_model.CpModel()
        self.solution_counter = VarArraySolutionCounter()

    # Create CSP Variables
    # Setup all Constraints depending on Board & Sudoku Rules
    def setup_csp(self, board: SudokuBoard):
        # initialize Board
        self.board = board._board
        self.board_size = board.size
        self.board_size_sqrt = board.size_sqrt
        # clean CSP environment
        self.model = cp_model.CpModel()
        self.solution_counter = VarArraySolutionCounter()
        self.variables = []
        self.solver_variables = []
        # Create all variables
        for i_x, row in enumerate(self.board):
            var_row = []
            for i_y, space in enumerate(row):
                var_name = "variable" + str(i_x) + "_" + str(i_y)
                var = self.model.NewIntVar(1, self.board_size, var_name)
                # Set Number if space is not empty
                if space != EMPTY_SPACE:
                    self.model.Add(var == space)
                var_row.append(var)
            self.variables.append(var_row)

        # Add constraints that each row, column and square holds different numbers
        columns = {}
        for row in self.variables:
            # Unique numbers in each row
            self.model.AddAllDifferent(row)
            for i_y, space in enumerate(row):
                # Create List for each Column
                if i_y in columns:
                    columns[i_y].append(space)
                else:
                    columns[i_y] = [space]

        # Unique numbers in each column
        for col in columns:
            self.model.AddAllDifferent(columns[col])

        for x_range in range(0, self.board_size, self.board_size_sqrt):
            for y_range in range(0, self.board_size, self.board_size_sqrt):
                # create Subgrid
                subgrid = []
                for x in range(x_range, x_range + self.board_size_sqrt):
                    for y in range(y_range, y_range + self.board_size_sqrt):
                        subgrid.append(self.variables[x][y])
                # Unique numbers in Subgrid
                self.model.AddAllDifferent(subgrid)

        # Convert 2 dimensional Variable list to 1 dimensional list
        for row in self.variables:
            for space in row:
                self.solver_variables.append(space)

    # Solve Sudoku
    # Save first found Solution in self.board
    def solve_csp(self, board: SudokuBoard, seed=None, decision_strategy=None, num_workers=None, log_stats=False):
        start = time.time()
        # create the model
        self.setup_csp(copy.deepcopy(board))
        # create the solver
        solver = cp_model.CpSolver()
        #solver.parameters.log_search_progress = True
        #solver.log_callback = print
        if num_workers:
            solver.parameters.num_search_workers = num_workers  # use x cores
        if decision_strategy:
            self.model.AddDecisionStrategy(self.solver_variables, decision_strategy, cp_model.SELECT_MIN_VALUE)
            solver.parameters.search_branching = cp_model.FIXED_SEARCH

        if seed:
            solver.parameters.random_seed = seed
        # find first solution
        status = solver.Solve(self.model)
        if status == cp_model.INFEASIBLE:
            print("ERROR: Model does not have a solution!")
        elif status == cp_model.FEASIBLE:
            print("Solution is FEASIBLE")
        elif status == cp_model.OPTIMAL:
            #print("Solution is OPTIMAL")
            # Create Sudoku Board from Solved Result
            for x in range(0, self.board_size):
                for y in range(0, self.board_size):
                    self.board[x][y] = solver.Value(self.variables[x][y])
            if log_stats:
                print()
                print()
                print('-----------CSP-Statistic ------------')
                print('Decision Strategy: ' + str(decision_strategy))
                print('Solution: Optimal')
                print('Number Branches: ' + str(solver.NumBranches()))
                print('Number Conflicts:' + str(solver.NumConflicts()))
                if num_workers:
                    print('Workers: ' + str(num_workers))
        else:
            print("ERROR: Solution Status unexpected!")
        end = time.time()
        if log_stats:
            print('Duration: ' + str(end - start) + 's')
            print('-------------------------------------')
            print(self)

    def __str__(self):
        """
        Returns a string representation of the board.
        """
        all_rows = []
        small_space = ' '
        big_space = '  '

        for x_i, row in enumerate(self.board):
            output = ''
            for y_i, field in enumerate(row):
                # add number
                output += str("." if field == 0 else field)
                # add space if not last number in row
                space = big_space
                if field > 9:
                    space = small_space
                if y_i < self.board_size - 1:
                    output += space
                    # add seperator at end of subgrid if not last number
                    if (y_i + 1) % self.board_size_sqrt == 0:
                        output += '| '
            # finish row
            all_rows.append(output)
            # add seperator at end of subgrid if not last row
            if ((x_i + 1) <= self.board_size - 1) and ((x_i + 1) % self.board_size_sqrt == 0):
                seperator = ''
                for char in output:
                    seperator += '-'
                all_rows.append(seperator)
        return '\n'.join(all_rows)

    # return number of unique & valid solutions
    # return -1 if no solution
    def get_num_solutions(self, board: SudokuBoard):
        # create the model
        self.setup_csp(board)
        # create the solver
        solver = cp_model.CpSolver()
        # find all solutions
        status = solver.SearchForAllSolutions(self.model, self.solution_counter)
        if status == cp_model.INFEASIBLE:
            #print("ERROR: Model does not have a solution!")
            return -1
        elif status == cp_model.FEASIBLE:
            #print("Solution is FEASIBLE")
            n = self.solution_counter.solution_count()
            #print("%d solution(s) found." % n)
            return n
        elif status == cp_model.OPTIMAL:
            #print("Solution is OPTIMAL")
            n = self.solution_counter.solution_count()
            #print("%d solution(s) found." % n)
            return n
        else:
            #print("ERROR: Solution Status unexpected!")
            return -1

    def generate_unique_sudoku(self, size=3, seed=None, return_removed_numbers=False):
        removed_numbers = 0
        # generate a fully solved board of size: size
        sb = SudokuBoard(size, seed=seed)
        self.solve_csp(sb, seed=seed)
        sb.set_board(self.board)
        # remove random numbers until
        # no unique solution
        new_sb = copy.deepcopy(sb)
        unique_solutuions = 1
        new_sb.remove_random_number()
        while unique_solutuions == 1:
            removed_numbers += 1
            new_sb.remove_random_number()
            unique_solutuions = self.get_num_solutions(new_sb)
            if unique_solutuions == 1:
                sb = copy.deepcopy(new_sb)
        # return last board with unique solution, and number of removed numbers if return_removed_numbers is True
        if return_removed_numbers:
            return sb, removed_numbers
        return sb
    
    def generate_random_sudoku(self, size=3, seed=None, remove_numbers=1):
        removed_numbers = 0
        # generate a fully solved board of size: size
        sb = SudokuBoard(size, seed=seed)
        self.solve_csp(sb, seed=seed)
        sb.set_board(self.board)

        # remove remove_numbers random numbers
        for i in range(remove_numbers):
            sb.remove_random_number()
        return sb

if __name__=="__main__":
    solver = CSP_Solver()

    # # create Board
    # board = SudokuBoard(2)
    # board._board[3, 0] = 4
    #
    # # Solve Board
    # solver.solve_csp(board)
    # # print solition
    # board.set_board(solver.board)
    # print(board)
    # print('----------------------------')

    # generate a Sudoku Board
    sb = solver.generate_unique_sudoku(3)
    #sb = solver.generate_random_sudoku(3, remove_numbers=70)


    #sb = SudokuBoard(n=3, seed=10)
    #sb._board[3,0] = 4

    print(sb)
    #print(solver.get_num_solutions(sb))

    # measure Time
    start = time.time()
    solver.solve_csp(sb, decision_strategy=None)
    # calculate elapsed Time
    end = time.time()
    print("CSP took: ", end - start, "seconds")
    print()

    start = time.time()
    solver.solve_csp(sb, decision_strategy=cp_model.CHOOSE_FIRST)
    # calculate elapsed Time
    end = time.time()
    print("CSP (CHOOSE_FIRST) took: ", end - start, "seconds")
    print()

    start = time.time()
    solver.solve_csp(sb, decision_strategy=cp_model.CHOOSE_MIN_DOMAIN_SIZE)
    # calculate elapsed Time
    end = time.time()
    print("CSP (CHOOSE_MIN_DOMAIN_SIZE) took: ", end - start, "seconds")
    print()

    start = time.time()
    solver.solve_csp(sb, decision_strategy=cp_model.CHOOSE_MAX_DOMAIN_SIZE)
    # calculate elapsed Time
    end = time.time()
    print("CSP (CHOOSE_MAX_DOMAIN_SIZE) took: ", end - start, "seconds")

    start = time.time()
    solver.solve_csp(sb, decision_strategy=None, num_workers=None)
    # calculate elapsed Time
    end = time.time()
    print("CSP took: ", end - start, "seconds")

    start = time.time()
    solver.solve_csp(sb, decision_strategy=None, num_workers=1)
    # calculate elapsed Time
    end = time.time()
    print("CSP (1) took: ", end - start, "seconds")

    start = time.time()
    solver.solve_csp(sb, decision_strategy=None, num_workers=3)
    # calculate elapsed Time
    end = time.time()
    print("CSP (3) took: ", end - start, "seconds")

    start = time.time()
    solver.solve_csp(sb, decision_strategy=None, num_workers=5)
    # calculate elapsed Time
    end = time.time()
    print("CSP (5) took: ", end - start, "seconds")