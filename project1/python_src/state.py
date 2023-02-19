import hashlib
import time

import numpy

from CombinedHeuristic import CombinedHeuristic
from OffensiveHeurisitics import OffensiveHeuristics
from DefensiveHeurisitcs import DefensiveHeuristics
from python_src.DefaultHeuristic import DefaultHeuristics

BLACK, WHITE, EMPTY = "B", "W", " "


class State:
    def __init__(self, width, height):
        self.board = [[WHITE] * width if i < 2 else
                    [BLACK] * width if i > height - 3 else 
                    [EMPTY] * width for i in range(height)
                    ]

        self.board = numpy.array(self.board)
        self.white_turn = True
        self.width = width
        self.height = height

    def __str__(self) -> str:
        dash_count = self.width * 4 - 3
        line = "\n" + "-" * dash_count + "\n"
        return line.join([ " | ".join([cell for cell in row]) for row in self.board[::-1]])

    def __hash__(self):
        """
        The numpy array stores the underlying data as bytes.
        This allows us to compute the hash of the state efficiently.
        """
        p = self.board.data.tobytes() + bytes(self.white_turn)
        hash_value = hashlib.md5(p).hexdigest()
        return int(hash_value, 16)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def index_2d(self, data, search):
        for i in range(len(data)):
            if search in data[i]:
                return i
        raise ValueError("{!r} is not in list".format(search))

    def is_terminal_state(self):
        """Check if this state is a terminal state"""
        distance_black = self.index_2d(self.board, BLACK)
        distance_white = self.index_2d(self.board[::-1], WHITE)
        if distance_black == 0 or distance_white == 0:
            return True
        return False

    @staticmethod
    def get_state_value(state, role):
        """Compute the value of the state based on the used heuristics"""
        return CombinedHeuristic.eval(state, role)
        #return DefaultHeuristics.eval(state, role)
