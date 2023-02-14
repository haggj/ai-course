
BLACK, WHITE, EMPTY = "B", "W", " "


class DefensiveHeuristics:

    @staticmethod
    def index_2d(data, search):
        for i in range(len(data)):
            if search in data[i]:
                return i

        return len(data)

    @staticmethod
    def eval(state, role):
        available_black = 0
        available_white = 0

        for i in range(len(state.board)):
            for j in range(len(state.board[0])):
                if state.board[i][j] == BLACK:
                    available_black += 1
                elif state.board[i][j] == WHITE:
                    available_white += 1

        distance_white = DefensiveHeuristics.index_2d(state.board[::-1], WHITE)
        distance_black = DefensiveHeuristics.index_2d(state.board, BLACK)

        if role == "white":
            if distance_white == 0:
                return 100
            if distance_black == 0:
                return -100
            return 2*available_white - available_black
        else:
            if distance_black == 0:
                return 100
            if distance_white == 0:
                return -100
            return 2*available_black - available_white

