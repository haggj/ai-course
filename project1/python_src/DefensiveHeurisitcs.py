
BLACK, WHITE, EMPTY = "B", "W", " "


class DefensiveHeuristics:
    """
    Try to protect own pieces and capture others.
    Do not consider how far the best piece moved.
    """

    @staticmethod
    def eval(state, role):
        board_height = len(state.board)
        available_black = 0
        available_white = 0
        distance_black = board_height
        distance_white = board_height

        # Loop over board to collect data used for evaluation
        for y in range(len(state.board)):
            for x in range(len(state.board[0])):
                if state.board[y][x] == BLACK:
                    # save the minimal distance to goal
                    distance_black = min(y, distance_black)
                    available_black += 1
                elif state.board[y][x] == WHITE:
                    # save the minimal distance to goal
                    distance_white = min(board_height-y-1, distance_white)
                    available_white += 1

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

