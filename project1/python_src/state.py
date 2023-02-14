import hashlib
import time

import numpy

from DefensiveHeurisitcs import DefensiveHeuristics
from DifferenceHeuristic import DifferenceHeuristic
from GPTHeuristic import GPTHeuristic
from Pieces_Progress import Pieces_Progress
from Pieces_Progress_v2 import Pieces_Progress_2

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
        distance_black = self.index_2d(self.board, BLACK)
        distance_white = self.index_2d(self.board[::-1], WHITE)
        if distance_black == 0 or distance_white == 0:
            return True
        return False

    @staticmethod
    def get_state_value(state, role):
        return DefensiveHeuristics.eval(state, role)


if __name__=="__main__":
    runs = 100000
    states = [State(6,6), State(7,7), State(8,8), State(9,9), State(10,10)]

    start = time.time()
    for i in range(runs//5):
        for state in states:
            hash(state)
    end = time.time()
    print(f"Took {round((end-start),3)}s")

