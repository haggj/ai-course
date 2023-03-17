from sudoku import SudokuBoard
from ortools.sat.python import cp_model

EMPTY_SPACE = 0

class CSP_Solver:
    def __init__(self, board=SudokuBoard(3)):
        self.board = board._board
        self.board_size = board.size
        self.board_size_sqrt = board.size_sqrt
        self.model = cp_model.CpModel()
        self.variables = []
        self.solver_variables = []
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

    def solve_csp(self):
        # create the model
        self.setup_csp()
        # create the solver
        solver = cp_model.CpSolver()
        status = solver.Solve(self.model)
        #solution_printer = cp_model.VarArraySolutionPrinter(self.solverVariables)
        # find all solutions and print them out
        #status = solver.SearchForAllSolutions(self.model, solution_printer)
        if status == cp_model.INFEASIBLE:
            print("ERROR: Model does not have a solution!")
        elif status == cp_model.MODEL_INVALID:
            print("ERROR: Model is invalid!")
            self.model.Validate()
        elif status == cp_model.UNKNOWN:
            print("ERROR: No solution was found!")
        else:
            #n = solution_printer.solution_count()
            #print("%d solution(s) found." % n)
            # Create Sudoku Board from Solved Result
            for x in range(0, self.board_size):
                for y in range(0, self.board_size):
                    self.board[x][y] = solver.Value(self.variables[x][y])
            #print(self.board)

board = SudokuBoard(3)
solver = CSP_Solver(board)
#solver.setup_csp()
solver.solve_csp()

board.set_board(solver.board)
print(board)