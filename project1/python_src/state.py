import hashlib
import time

import numpy

from DefensiveHeurisitcs import DefensiveHeuristics
from DifferenceHeuristic import DifferenceHeuristic
from GPTHeuristic import GPTHeuristic
from Pieces_Progress import Pieces_Progress
from Pieces_Progress_v2 import Pieces_Progress_2
from CombinedHeuristic import CombinedHeuristic
from OffensiveHeurisitics import OffensiveHeuristics
from DefensiveHeurisitcs import DefensiveHeuristics

import random

zobTable = [[[random.randint(1,2**64 - 1) for i in range(2)]for j in range(10)]for k in range(10)]

def indexing(piece):
    ''' mapping each piece to a particular number'''
    if (piece=='B'):
        return 0
    if (piece=='W'):
        return 1
    else:
        return -1

def computeHash(board):
    h = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != ' ':
                piece = indexing(board[i][j])
                h ^= zobTable[i][j][piece]
    return h

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
        #p = self.board.data.tobytes() + bytes(self.white_turn)
        #hash_value = hashlib.md5(p).hexdigest()

        #return int(hash_value, 16)
        return computeHash(self.board)

    def __eq__(self, other):
        return hash(self) == hash(other)

    @staticmethod
    def get_state_value(state, role):
        return CombinedHeuristic.eval(state, role)


if __name__=="__main__":
    runs = 100000
    states = [State(6,6), State(7,7), State(8,8), State(9,9), State(10,10)]

    start = time.time()
    for i in range(runs//5):
        for state in states:
            hash(state)
    end = time.time()
    print(f"Took {round((end-start),3)}s")

