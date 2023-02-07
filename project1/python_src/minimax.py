import sys
import time
from copy import deepcopy

from environment import Environment

INF = sys.maxsize

class MiniMax:
    """Minimax with iterative deepening"""

    def __init__(self, env: Environment, heuristic, role, play_clock=10):
        self.env = env
        self.heuristic = heuristic
        self.cached_states = {}
        self.role = role
        self.play_clock = 30 * 0.99


    def init_stats(self):
        self.state_expansions = 0
        self.start = time.time()
        self.max_depth = 1

    def print_stats(self):
        end = time.time()
        print("\n\n\nStats of MiniMax")
        print("Expanded states: " + str(self.state_expansions))
        print("Max depth: " + str(self.max_depth - 1))
        print("Duration: " + str(end - self.start))
        print("States/Second: " + str(self.state_expansions / (end - self.start)))
        print("Cached states: " + str(len(self.cached_states)))

    def run(self):
        self.init_stats()

        # Run MiniMax using Iterative Deepening (until TimeoutError is raised)
        max_value, max_action = -INF, None
        try:
            while True:
                value, action = self.minmax(self.env.current_state, self.max_depth, -INF, INF, True)
                self.max_depth += 1

                # Abort search if winning move was found
                if value == 100:
                    max_value, max_action = value, action
                    break

                # Only update value if better action was found
                if value > max_value:
                    max_value, max_action = value, action
                # if self.max_depth == 6:
                #     break
        except TimeoutError:
            pass

        self.print_stats()
        return max_action

    def get_successors(self, state):
        legal_moves = self.env.get_legal_moves(state)
        for next_action in legal_moves:
            next_state = deepcopy(self.env.current_state)
            self.env.move(next_state, next_action)
            yield next_state, next_action

    def minmax(self, state, depth, alpha, beta, max_player):
        action = None
        self.state_expansions += 1

        if (time.time() - self.start) > self.play_clock:
            # Stop the search
            raise TimeoutError()

        if depth == 0:
            return self.heuristic(state, []), action

        if max_player:
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
                if value < beta:
                    beta, action = value, next_action
                if beta <= alpha:
                    break
            return min_value, action



