import hashlib
from copy import deepcopy

from project2.sudoku import SudokuBoard
from queue import LifoQueue


class SudokuDFS:
    def __init__(self, board: SudokuBoard):
        self.state = board

    def solve(self):
        state = self.state
        queue = LifoQueue()
        queue.put(state)
        visited = {}
        visits = 0

        while True:
            state = queue.get(False)

            if state in visited:
                print("revisited state")
                continue
            visited[state] = True

            visits += 1

            print(state)
            print()
            print()
            if visits%1000==0:
                print(visits)

            # Termination condition
            if state.is_complete():
                print(visits)
                return state

            # Append next moves
            legal_moves = state.get_legal_moves()
            for move in legal_moves:
                next_state : SudokuBoard = deepcopy(state)
                next_state.apply_move(move)
                queue.put(next_state)


sb = SudokuBoard(n=3)
sb._board[3,0] = 4

dfs = SudokuDFS(board=sb)
print(dfs.solve())
