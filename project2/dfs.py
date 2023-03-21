import time
from copy import deepcopy

from CSP_Solver import CSP_Solver
from sudoku import SudokuBoard, Version
from queue import LifoQueue


class SudokuDFS:
    def __init__(self, board: SudokuBoard):
        self.state = board
        self.reset_stats()

    def reset_stats(self):
        self.visited_states = {}
        self.revistited_states = 0
        self.node_expansions = 0
        self.start_time = time.time()
        self.branches = 0

    def print_stats(self, version, final=True):
        duration = round(time.time() - self.start_time, 5)

        heading = "Statistic " if final else "Debug "
        heading += str(version)
        msg = f"-------------{heading}--------------"
        print("\n\n" + msg)
        print(f"Node expansions: {self.node_expansions}")
        print(f"Expansions/second: {self.node_expansions/duration}")
        print(f"Average branching factor: {self.branches//self.node_expansions}")
        print(f"Revisited states: {self.revistited_states}")
        print(f"Duration: {duration}s")
        print("-"*len(msg))

    def solve(self, version=Version.IMPROVED):
        self.reset_stats()
        state = deepcopy(self.state)
        queue = LifoQueue()
        queue.put(state)

        while True:
            state = queue.get(False)

            if state in self.visited_states:
                continue
            self.visited_states[state] = True
            self.node_expansions += 1

            # Debug information
            if self.node_expansions % 1000 == 0:
                self.print_stats(version, False)
                print(state)
                # exit()

            # Termination condition
            if state.is_complete():
                self.print_stats(version, True)
                return state

            # Append next moves
            for move in state.get_legal_moves(version):
                self.branches += 1
                next_state: SudokuBoard = deepcopy(state)
                next_state.apply_move(move)
                queue.put(next_state)

    def solve_recursive(self, state: SudokuBoard, version=Version.IMPROVED):
        if state in self.visited_states:
            return None
        self.visited_states[state] = True
        self.node_expansions += 1

        # Termination condition
        if state.is_complete():
            return state
        
        # Debug information
        if self.node_expansions % 1000 == 0:
            self.print_stats(version, False)
            print(state)

        # Append next moves
        for move in state.get_legal_moves(version):
            self.branches += 1
            #next_state: SudokuBoard = deepcopy(state)
            #next_state.apply_move(move)
            state.apply_move(move)
            result = self.solve_recursive(state, version)
            if state.is_complete():
                return state
            else:
                state.undo_move(move)
            if result is not None:
                return result

        return None

# Generate sudoku via CSP solver
solver = CSP_Solver()
sudoku = solver.generate_unique_sudoku(3)


# Generate sudoku manually
sudoku = SudokuBoard(n=3)
sudoku._board[3,0] = 4
print(sudoku)

dfs = SudokuDFS(board=sudoku)
#print(dfs.solve(Version.IMPROVED))
print(dfs.solve_recursive(sudoku,Version.IMPROVED))
# print(dfs.solve(Version.NAIVE))
