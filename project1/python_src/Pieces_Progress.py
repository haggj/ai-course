
BLACK, WHITE, EMPTY = "B", "W", " "
class Pieces_Progress:
    @staticmethod
    def eval(state):
        distance_black = Pieces_Progress.index_2d(state.board, BLACK)
        distance_white = Pieces_Progress.index_2d(state.board[::-1], WHITE)
        if distance_black == 0:
            return -100
        if distance_white == 0:
            return 100
        num_black, num_white = Pieces_Progress.count_knights(state.board)
        return distance_black - distance_white + num_white - num_black

    @staticmethod
    def index_2d(data, search):
        for i in range(len(data)):
            if search in data[i]:
                return i
        raise ValueError("{!r} is not in list".format(search))

    def count_knights(board):
        num_black = 0
        num_white = 0
        for row in board:
            for field in row:
                if field == 'W':
                    num_white += 1
                elif field == 'B':
                    num_black += 1
        return num_black, num_white