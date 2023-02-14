
BLACK, WHITE, EMPTY = "B", "W", " "


class OffensiveHeuristics:
    """
    Try to move forward in the field.
    Do not consider captures at all.
    """

    @staticmethod
    def eval(state, role):
        board_height = len(state.board)
        distance_black = board_height
        distance_white = board_height

        for y in range(len(state.board)):
            for x in range(len(state.board[0])):
                if state.board[y][x] == BLACK:
                    distance_black = min(y, distance_black)
                elif state.board[y][x] == WHITE:
                    distance_white = min(board_height-y-1, distance_white)

        if role == "white":
            if distance_white == 0:
                return 100
            if distance_black == 0:
                return -100
            return board_height-distance_white
        else:
            if distance_black == 0:
                return 100
            if distance_white == 0:
                return -100
            return board_height-distance_black

