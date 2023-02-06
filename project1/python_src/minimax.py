import sys
import time
from copy import deepcopy

from environment import Environment

INF = sys.maxsize

class MiniMax:
    """Minimax with iterative deepening"""

    def __init__(self, env: Environment, heuristic, max_time=5):
        self.env = env
        self.heuristic = heuristic
        self.cached_states = {}
        self.max_time = max_time

    def run(self):
        # Reset stats
        self.state_expansions = 0
        self.max_depth = 0
        self.start = time.time()

        # Run MiniMax using Iterative Deepening (until TimeoutError is raised)
        depth = 1
        value, action = None, None
        try:
            while True:
                value, action = self.minmax(self.env.current_state, depth, -INF, INF, True)
                depth += 1
        except TimeoutError:
            pass


        # Print stats
        end = time.time()
        print("\n\n\nStats of MiniMax")
        print("Expanded states: " + str(self.state_expansions))
        print("Max depth: " + str(self.max_depth))
        print("Duration: " + str(end - self.start))
        print("States/Second: " + str(self.state_expansions/(end - self.start)))
        print("Cached states: " + str(len(self.cached_states)))
        return action

    def get_successors(self, state):
        legal_moves = self.env.get_legal_moves(state)
        for move in legal_moves:
            self.env.move(state, move)
            if self.env.current_state not in self.cached_states:
                self.cached_states[self.env.current_state] = deepcopy(self.env.current_state)
            yield self.cached_states[self.env.current_state], move

            self.env.undo_move(state, move)

    def minmax(self, state, depth, alpha, beta, white_player):
        action = None
        self.state_expansions += 1
        self.max_depth = max(self.max_depth, depth)

        if (time.time() - self.start) > self.max_time:
            # Stop the search
            raise TimeoutError()

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



