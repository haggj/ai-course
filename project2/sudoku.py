import hashlib

import numpy as np

EMPTY_SPACE = 0

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

    def get_row(self, row):
        if not isinstance(row, int) or row < 0 or row >= self.size:
            raise Exception('Invalid row: ' + str(row))

        return [self._board[x][row] for x in range(self.size)]

    def __str__(self):
        """Returns a string representation of the board.
        """
        symbol_length = len(str(self.size_sqrt))

        all_rows = []

        for y in range(self.size):
            row = list(self.get_row(y))

            # Add vertical separators to the row.
            for i in range(self.size - 1 - self.size_sqrt, -1, -self.size_sqrt):
                row.insert(i + 1, '|')

            # Go through the row and make sure it is properly spaced if
            # symbols can have multiple digits.
            if self.size > 9:
                for i, symbol in enumerate(row):
                    row[i] = symbol.rjust(symbol_length)

            all_rows.append(' '.join(['.' if e == 0 else str(e) for e in row]))

            # Add a horizontal separator, if needed.
            if (y + 1) % self.size_sqrt == 0 and y != (self.size - 1):
                all_rows.append('-' * ((symbol_length  * 2 * self.size_sqrt * self.size_sqrt + self.size_sqrt + 1 - (4 - self.size_sqrt))))

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

    def get_legal_moves(self):
        """
        Returns a list of legal moves for the current state.
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
                            fields.add((x,y))
                    self._board[x][y] = EMPTY_SPACE

        if len(fields) == empty_fields:
            return legal_moves
        # If there is not a valid move for each field no solution exists
        return []

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