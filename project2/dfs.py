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
        self.branching_factor = 0
        self.branches = 0
        self.invalid_states = 0

    def print_stats(self, version, final=True, recursive=False):
        duration = round(time.time() - self.start_time, 5)

        heading = "Statistic " if final else "Debug "
        msg = f"-------------{heading}--------------"

        print("\n\n" + msg)
        print("Version: " + str(version))
        print("Recursion: " + str(recursive))
        print(f"Node expansions: {self.node_expansions}")
        print(f"Expansions/second: {self.node_expansions/duration}")
        print(f"Average branching factor: {self.branching_factor}")
        print(f"Revisited states: {self.revistited_states}")
        print(f"Invalid states: {self.invalid_states}")
        print(f"Duration: {duration}s")
        print("-"*len(msg))

    def update_branching_factor(self, val):
        if val == 0:
            self.invalid_states += 1
            return

        if self.branching_factor == 0:
            self.branches = 1
            self.branching_factor = val
        else:
            # Update average branching factor: https://math.stackexchange.com/a/957376
            self.branches += 1
            self.branching_factor = self.branching_factor + ((val - self.branching_factor) / self.branches)

    def solve(self, version=Version.IMPROVED):
        self.reset_stats()
        state = deepcopy(self.state)
        queue = LifoQueue()
        queue.put(state)

        while True:
            state = queue.get(False)

            if state in self.visited_states:
                self.revistited_states += 1
                continue
            self.visited_states[state] = True
            self.node_expansions += 1

            # Debug information
            if self.node_expansions % 1000 == 0:
                self.print_stats(version, False)
                print(state)

            # Termination condition
            if state.is_complete():
                self.print_stats(version, True)
                print(state)
                return state

            # Append next moves
            legal_moves = state.get_legal_moves(version)
            self.update_branching_factor(len(legal_moves))
            for move in state.get_legal_moves(version):
                next_state: SudokuBoard = deepcopy(state)
                next_state.apply_move(move)
                queue.put(next_state)

    def solve_recursive(self, state: SudokuBoard, version=Version.IMPROVED):
        self.reset_stats()
        solution = self._solve_recursive(deepcopy(state), version)
        if not solution:
            raise Exception("Could not find solution...")
        return solution

    def _solve_recursive(self, state: SudokuBoard, version=Version.IMPROVED):

        if state in self.visited_states:
            self.revistited_states += 1
            return None

        # Store the hash of the object in the dict, because we are operating on the same object
        # all the time. This messes with the detection, if the current state was analyzed before
        # if using self.visited_states[state] = True
        self.visited_states[hash(state)] = True
        self.node_expansions += 1

        # Termination condition
        if state.is_complete():
            self.print_stats(version, True, True)
            print(state)
            return state

        # Debug information
        if self.node_expansions % 1000 == 0:
            self.print_stats(version, False, True)
            print(state)

        # Append next moves
        legal_moves = state.get_legal_moves(version)
        legal_moves.reverse()
        self.update_branching_factor(len(legal_moves))
        for move in legal_moves:
            state.apply_move(move)
            result = self._solve_recursive(state, version)
            if result:
                return result
            state.undo_move(move)
        return None

# Generate sudoku via CSP solver
solver = CSP_Solver()
sudoku = solver.generate_unique_sudoku(3, 40)

# Generate sudoku manually
sudoku = SudokuBoard(n=3, seed=10)
print(sudoku)


# CSP solver
solver.solve_csp(deepcopy(sudoku))

dfs = SudokuDFS(board=sudoku)
sol1 = dfs.solve(Version.SORTED)
sol2 = dfs.solve(Version.STORE_LEGAL)
sol3 = dfs.solve_recursive(sudoku, Version.SORTED)
sol4 = dfs.solve_recursive(sudoku, Version.STORE_LEGAL)
assert sol1 == sol2
assert sol2 == sol3
assert sol3 == sol4
