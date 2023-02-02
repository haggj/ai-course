import sys
from copy import deepcopy

from environment import Environment

INF = sys.maxsize

class MiniMax:
    """Minimax with iterative deepening"""

    def __init__(self, env: Environment, heuristic):
        self.env = env
        self.heuristic = heuristic

    def run(self):
        value, action = self.minmax(self.env.current_state, 4, -INF, INF, True)
        return action

    def get_successors(self, state):
        legal_moves = self.env.get_legal_moves(state)
        for move in legal_moves:
            self.env.move(state, move)
            yield (deepcopy(self.env.current_state), move)
            self.env.undo_move(state, move)

    def minmax(self, state, depth, alpha, beta, white_player):
        action = None

        if depth == 0:
            return self.heuristic(state, []), action

        if white_player:
            max_value = -INF
            for next_state, next_action in self.get_successors(state):
                value, _ = self.minmax(next_state, depth-1, alpha, beta, False)
                max_value = max(max_value, value)
                if value > alpha:
                    alpha, action = value, next_action
                if beta <= alpha:
                    break
            return max_value, action
        else:
            min_value = INF
            for next_state, next_action in self.get_successors(state):
                value, _ = self.minmax(next_state, depth - 1, alpha, beta, True)
                min_value = min(min_value, value)
                beta = min(beta, value)
                if value < beta:
                    beta, action = value, next_action
                if beta <= alpha:
                    break
            return min_value, action



