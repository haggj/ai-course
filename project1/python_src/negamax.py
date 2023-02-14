import collections
import sys
import time
from copy import deepcopy

from environment import Environment
from state import State

INF = sys.maxsize

# Entry object which is stored in the transition table
Entry = collections.namedtuple('Entry', ['value', 'flag', 'depth'])


class NegaMax:
    """Negamax with iterative deepening."""

    def __init__(self, env: Environment, role, play_clock):
        self.env = env
        self.role = role
        self.play_clock = play_clock * 0.99
        self.transition_table = {}

    def init_stats(self):
        """Initialize stats."""
        self.state_expansions = 0
        self.start = time.time()
        self.timeStamps = []
        self.max_depth = 1
        self.transition_table_hits = 0

    def print_stats(self):
        """Print the collected stats."""
        end = time.time()
        print("\n\n\nStats of MiniMax / NegaMax")
        print("Expanded states: " + str(self.state_expansions))
        print("Max depth: " + str(self.max_depth - 1))
        print("Total Duration: " + str(end - self.start))
        for t in self.timeStamps:
            print(t)
        print("States/Second: " + str(self.state_expansions / (end - self.start)))
        print("Transition table hits: " + str(self.transition_table_hits))
        print(self.role)

    def run(self):
        """
        Run the Negamax algorithm using Iterative Deepening until Timeout occurs.
        Returns the best action found by the algorithm.
        """
        self.init_stats()
        max_value, max_action = -INF, None
        negamax_color = 1
        root_state = deepcopy(self.env.current_state)

        # Run MiniMax using Iterative Deepening (until TimeoutError is raised)
        try:
            while True:
                max_value, max_action = self.start_negamax(
                    node=root_state,
                    depth=self.max_depth,
                    alpha=-INF,
                    beta=INF,
                    color=negamax_color)
                self.timeStamps.append("\tDepth-" + str(self.max_depth) + ": " + str(time.time() - self.start) + " s")
                self.max_depth += 1
                
                # Break Negamax, if a winning move was found.
                if max_value == 100:
                    break

        except TimeoutError:
            # Timeout indicates that our time is over, return best move
            pass

        self.print_stats()
        return max_action

    def _store_transition_table(self, node, value, alpha_orig, beta, depth):
        """Helper function to store node in transition table."""
        if value <= alpha_orig:
            flag = "upper"
        elif value >= beta:
            flag = "lower"
        else:
            flag = "exact"
        self.transition_table[node] = Entry(value=value, depth=depth, flag=flag)

    def start_negamax(self, node, depth, alpha, beta, color):
        """
        Start negamax algorithm. The expansion of the first depth is not done in the
        recursive function because we need to keep track of the applied action here.
        This allows us to return the action associated with the found value.
        """
        action = None
        value = -INF

        for next_action in self.env.get_legal_moves(node):
            self.env.move(node, next_action)
            res = self.negamax(node, depth - 1, -beta, -alpha, -color)
            self.env.undo_move(node, next_action)
            if -res > value:
                action = next_action
            value = max(value, -res)
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        return value, action

    def negamax(self, node, depth, alpha, beta, color):
        """
        Recursive NegaMax function. Computes the best value of the given node.
        """
        self.state_expansions += 1

        if (time.time() - self.start) > self.play_clock:
            raise TimeoutError() # Stop the search

        # Transition table lookup
        alpha_orig = alpha
        entry = self.transition_table.get(node)
        if entry and entry.depth >= depth:
            self.transition_table_hits += 1
            if entry.flag == "exact":
                return entry.value
            elif entry.flag == "lower":
                alpha = max(alpha, entry.value)
            elif entry.flag == "upper":
                beta = min(beta, entry.value)

            if alpha >= beta:
                return entry.value

        # Termination condition
        value = State.get_state_value(node, self.role)
        if depth == 0 or value == 100 or value == -100:
            value = color * value
            self._store_transition_table(node, value, alpha_orig, beta, depth)
            return value

        # Recursion
        value = -INF
        for next_action in self.env.get_legal_moves(node):
            self.env.move(node, next_action)
            res = self.negamax(node, depth - 1, -beta, -alpha, -color)
            self.env.undo_move(node, next_action)
            value = max(value, -res)
            alpha = max(alpha, value)
            if alpha >= beta:
                break

        # Transition table store
        self._store_transition_table(node, value, alpha_orig, beta, depth)
        return value



