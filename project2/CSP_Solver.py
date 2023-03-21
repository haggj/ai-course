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
    def setup_csp(self):
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
    def solve_csp(self, board: SudokuBoard):
        # initialize Board
        self.board = board._board
        self.board_size = board.size
        self.board_size_sqrt = board.size_sqrt
        # create the model
        self.setup_csp()
        # create the solver
        solver = cp_model.CpSolver()
        # find first solution
        status = solver.Solve(self.model)
        if status == cp_model.INFEASIBLE:
            print("ERROR: Model does not have a solution!")
        elif status == cp_model.FEASIBLE:
            print("Solution is FEASIBLE")
        elif status == cp_model.OPTIMAL:
            print("Solution is OPTIMAL")
            # Create Sudoku Board from Solved Result
            for x in range(0, self.board_size):
                for y in range(0, self.board_size):
                    self.board[x][y] = solver.Value(self.variables[x][y])
        else:
            print("ERROR: Solution Status unexpected!")

    # return number of unique & valid solutions
    # return -1 if no solution
    def get_num_solutions(self, board: SudokuBoard):
        # initialize Board
        self.board = board
        self.board = board._board
        self.board_size = board.size
        self.board_size_sqrt = board.size_sqrt
        # create the model
        self.setup_csp()
        # create the solver
        solver = cp_model.CpSolver()
        # find all solutions
        status = solver.SearchForAllSolutions(self.model, self.solution_counter)
        if status == cp_model.INFEASIBLE:
            print("ERROR: Model does not have a solution!")
            return -1
        elif status == cp_model.FEASIBLE:
            print("Solution is FEASIBLE")
            n = self.solution_counter.solution_count()
            print("%d solution(s) found." % n)
            return n
        elif status == cp_model.OPTIMAL:
            print("Solution is OPTIMAL")
            n = self.solution_counter.solution_count()
            print("%d solution(s) found." % n)
            return n
        else:
            print("ERROR: Solution Status unexpected!")
            return -1


if __name__=="__main__":
    # measure Time
    start = time.time()

    # create Board
    board = SudokuBoard(3)
    solver = CSP_Solver()

    # Solve Board
    solver.solve_csp(board)
    # print solition
    board.set_board(solver.board)
    print(board)
    print('----------------------------')

    # remove random number until
    # no unique solution
    print('remove 5 random numbers\n')
    for i in range(5):
        board.remove_random_number()
    print(board)
    solver.solve_csp(board)
    #print(solver.get_num_solutions(board))

    # calculate elapsed Time
    end = time.time()
    print("CSP took: ", end - start, "seconds")