import hashlib
from enum import Enum
from itertools import chain

import numpy as np
import random

EMPTY_SPACE = 0

class Version(Enum):
    NAIVE = "Naive"
    IMPROVED = "Improved"
    SORTED = "Sorted"

class SudokuBoard:

    def __init__(self, n=3):
        self.size = n*n
        self.size_sqrt = n
        self._board = [[EMPTY_SPACE] * self.size for i in range(self.size)]  # create an empty board
        self._board = np.array(self._board)

    def __hash__(self):
        """
        The numpy array stores the underlying data as bytes.
        This allows us to compute the hash of the state efficiently.
        """
        p = self._board.data.tobytes()
        hash_value = hashlib.md5(p).hexdigest()
        return int(hash_value, 16)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def set_board(self, board):
        self._board = board

    def get_row(self, row):
        if not isinstance(row, int) or row < 0 or row >= self.size:
            raise Exception('Invalid row: ' + str(row))

        return [self._board[x][row] for x in range(self.size)]

    def __str__(self):
        """Returns a string representation of the board.
        """
        all_rows = []
        small_space = ' '
        big_space = '  '

        for x_i, row in enumerate(self._board):
            output = ''
            for y_i, field in enumerate(row):
                # add number
                output += str(field)
                # add space if not last number in row
                space = big_space
                if field > 9:
                    space = small_space
                if y_i < self.size - 1:
                    output += space
                    # add seperator at end of subgrid if not last number
                    if (y_i + 1) % self.size_sqrt == 0:
                        output += '| '
            # finish row
            all_rows.append(output)
            # add seperator at end of subgrid if not last row
            if ((x_i + 1) <= self.size - 1) and ((x_i + 1) % self.size_sqrt == 0):
                seperator = ''
                for char in output:
                    seperator += '-'
                all_rows.append(seperator)
        return '\n'.join(all_rows)
    
    def is_legal_state(self):
        """
        Check if this state is a legal state.
        """
        # Check if the numbers are unique in each row
        for row in self._board:
            if len(np.unique(row[row!=0])) != len(np.nonzero(row)[0]):
                return False
            
        # Check if the numbers are unique in each column
        for col in self._board.T:
            if len(np.unique(col[col!=0])) != len(np.nonzero(col)[0]):
                return False
            
        # Check if the numbers are unique in each subgrid
        for i in range(0, self.size, self.size_sqrt):
            for j in range(0, self.size, self.size_sqrt):
                subgrid = self._board[i:i+self.size_sqrt, j:j+self.size_sqrt]
                if len(np.unique(subgrid[subgrid!=0])) != len(np.nonzero(subgrid)[0]):
                    return False
        
        return True

    def naive_get_legal_moves(self):
        """
        Test for each empty field and each number if the resulting board is in a legal state.
        This function iterates over the whole board to detect empty fields. It then iterates over
        all possible values and applies them to the field. For each combination of empty field and
        possible value, the function self.is_legal_state() is called.
        """
        legal_moves = []
        fields = set()
        empty_fields = 0

        for x in range(self.size):
            for y in range(self.size):
                if self._board[x][y] == EMPTY_SPACE:
                    empty_fields += 1
                    for i in range(1, self.size + 1):
                        self._board[x][y] = i
                        if self.is_legal_state():
                            legal_moves.append((x, y, i))
                            fields.add((x, y))
                    self._board[x][y] = EMPTY_SPACE

        if len(fields) == empty_fields:
            return legal_moves
        # If there is not a valid move for each field no solution exists
        return []

    def improved_get_legal_moves(self, version):
        """
        Idea: Reduce calls to self.is_legal_state() by considering the existing values in the board.
        """
        allowed_values = set([i for i in range(1, self.size+1)])

        rows = [allowed_values.difference(set(row)) for row in self._board]
        cols = [allowed_values.difference(set(col)) for col in self._board.T]

        subgrids = []
        for i in range(0, self.size, self.size_sqrt):
            for j in range(0, self.size, self.size_sqrt):
                off = self.size_sqrt
                subgrids.append(allowed_values - set(np.unique(self._board[i:i+off, j:j+off])))

        def get_subgrid_index(x,y):
            return int(x//self.size_sqrt)*self.size_sqrt + int(y//self.size_sqrt)

        legal_moves = {}

        for x in range(self.size):
            for y in range(self.size):
                if self._board[x][y] == EMPTY_SPACE:
                    subgrid = subgrids[get_subgrid_index(x,y)]
                    possible_values = rows[x].intersection(cols[y]).intersection(subgrid)
                    if not possible_values:
                        # If there is not a valid move for each field no solution can be found
                        return []
                    for i in possible_values:
                        legal_moves.setdefault((x, y), []).append((x, y, i))

        if version == Version.SORTED:
            sorted_list = sorted(legal_moves.values(), reverse=True, key=len)
            res = list(chain.from_iterable(sorted_list))
        else:
            res = list(chain.from_iterable(legal_moves.values()))
        return res


    def get_legal_moves(self, version: Version = Version.NAIVE):
        """
        Returns a list of legal moves for the current state.
        """
        if version == Version.NAIVE:
            return self.naive_get_legal_moves()
        else:
            return self.improved_get_legal_moves(version)


    def get_first_legal_move(self):
        """
        Returns the first legal move for the current state.
        """
        legal_moves = []

        for x in range(self.size):
            for y in range(self.size):
                if self._board[x][y] == EMPTY_SPACE:
                    for i in range(1, self.size + 1):
                        self._board[x][y] = i
                        if self.is_legal_state():
                            return (x, y, i)
                    self._board[x][y] = EMPTY_SPACE

        raise Exception("No legal move found.")

    def apply_move(self, move):
        x, y, val = move
        self._board[x][y] = val

    def undo_move(self, move):
        x, y, val = move
        self._board[x][y] = EMPTY_SPACE

    def is_complete(self):
        for x in range(self.size):
            for y in range(self.size):
                if self._board[x][y] == EMPTY_SPACE:
                    return False
        if self.is_legal_state():
            return True
        raise Exception("Board complete but no in legal state.")

    # removes a random number from board
    def remove_random_number(self):
        x = random.randrange(0, self.size)
        y = random.randrange(0, self.size)
        # if random field is not null remove number
        if self._board[x][y] != 0:
            self._board[x][y] = 0
        # repeat until none empty field found
        else:
            # TODO: !!! Infinite Loop on empty board !!!
            self.remove_random_number()


if __name__=="__main__":
    sb = SudokuBoard(n=3)
    sb._board[3,0] = 4
    while not sb.is_complete():
        sb.apply_move(sb.get_first_legal_move())
        print()
        print()
        print(sb)
    exit()


    print(sb)
    sb.apply_move(sb.get_first_legal_move())
    print()
    print()
    print(sb)

    sb2 = SudokuBoard(n=3)
    legal_moves_2 = sb2.get_legal_moves()

    diff = []
    for element in legal_moves_2:
        if element not in legal_moves:
            diff.append(element)

    print(diff)