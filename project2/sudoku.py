EMPTY_SPACE = '.'
class SudokuBoard:

    def __init__(self, n=3):
        self.size = n*n
        self.size_sqrt = n
        self._board = [[EMPTY_SPACE] * self.size for i in range(self.size)]  # create an empty board

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

            all_rows.append(' '.join(row))

            # Add a horizontal separator, if needed.
            if (y + 1) % self.size_sqrt == 0 and y != (self.size - 1):
                all_rows.append('-' * ((symbol_length * self.size_sqrt + self.size_sqrt+1) * self.size_sqrt + 1))

        return '\n'.join(all_rows)


print(SudokuBoard(n=4))