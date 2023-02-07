import collections
import sys
import time
from copy import deepcopy

from environment import Environment
from state import State

INF = sys.maxsize

Entry = collections.namedtuple('Entry', ['value', 'flag', 'depth'])


class MiniMax:
    """Minimax/Negamax with iterative deepening"""

    def __init__(self, env: Environment, role, play_clock):
        self.env = env
        self.role = role
        self.play_clock = play_clock * 0.99
        self.transition_table = {}


    def init_stats(self):
        self.state_expansions = 0
        self.start = time.time()
        self.max_depth = 1
        self.transition_table_hits = 0

    def print_stats(self):
        end = time.time()
        print("\n\n\nStats of MiniMax")
        print("Expanded states: " + str(self.state_expansions))
        print("Max depth: " + str(self.max_depth - 1))
        print("Duration: " + str(end - self.start))
        print("States/Second: " + str(self.state_expansions / (end - self.start)))
        print("Transition table hits: " + str(self.transition_table_hits))

    def run(self):
        self.init_stats()

        # Run MiniMax using Iterative Deepening (until TimeoutError is raised)
        max_value, max_action = -INF, None
        try:
            while True:
                value, action = self.negamax(self.env.current_state, self.max_depth, -INF, INF,  1 if self.role == "white" else -1)
                max_value, max_action = value, action
                self.max_depth += 1

                # if self.max_depth == 5:
                #     break
        except TimeoutError:
            pass

        self.print_stats()
        return max_action

    def get_successors(self, state):
        legal_moves = self.env.get_legal_moves(state)
        for next_action in legal_moves:
            next_state = deepcopy(state)
            self.env.move(next_state, next_action)
            yield next_state, next_action

    def negamax(self, node, depth, alpha, beta, color):
        action = None
        self.state_expansions += 1

        if (time.time() - self.start) > self.play_clock:
            # Stop the search
            raise TimeoutError()

        # Transition table lookup
        alpha_orig = alpha
        if False and node in self.transition_table:
            entry = self.transition_table[node]
            if entry.depth >= depth:
                if entry.flag == "exact":
                    return entry.value, None
                elif entry.flag == "lower":
                    alpha = max(alpha, entry.value)
                elif entry.flag == "upper":
                    beta = min(beta, entry.value)

                if alpha >= beta:
                    return entry.value, None

        # Termination condition
        if depth == 0 or node.is_terminal_state():
            return color * State.get_state_value(node), None

        # Recursion
        value = -INF
        for next_state, next_action in self.get_successors(node):
            res, _ = self.negamax(next_state, depth - 1, -beta, -alpha, -color)
            if -res > value:
                action = next_action
            value = max(value, -res)
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        # Transition table store
        if value <= alpha_orig:
            flag = "upper"
        elif value >= beta:
            flag = "lower"
        else:
            flag = "exact"
        self.transition_table[node] = Entry(value=value, depth=depth, flag=flag)

        return value, action

    # def minimax(self, state, depth, alpha, beta, max_player):
    #     action = None
    #     self.state_expansions += 1
    #
    #     if (time.time() - self.start) > self.play_clock:
    #         # Stop the search
    #         raise TimeoutError()
    #
    #     if depth == 0:
    #         return State.get_state_value(state), action
    #
    #     if max_player:
    #         max_value = -INF
    #         for next_state, next_action in self.get_successors(state):
    #             value, _ = self.minimax(next_state, depth - 1, alpha, beta, False)
    #             max_value = max(max_value, value)
    #             if value > alpha:
    #                 alpha, action = value, next_action
    #             if beta <= alpha:
    #                 break
    #         return max_value, action
    #     else:
    #         min_value = INF
    #         for next_state, next_action in self.get_successors(state):
    #             value, _ = self.minimax(next_state, depth - 1, alpha, beta, True)
    #             min_value = min(min_value, value)
    #             if value < beta:
    #                 beta, action = value, next_action
    #             if beta <= alpha:
    #                 break
    #         return min_value, action



