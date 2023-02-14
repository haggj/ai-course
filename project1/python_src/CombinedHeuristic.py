
BLACK, WHITE, EMPTY = "B", "W", " "


class CombinedHeuristic:

    @staticmethod
    def eval(state, role):
        # max distance & number of rows
        board_size = len(state.board)

        # initial variables
        available_black = 0
        available_white = 0
        distance_black = board_size
        distance_white = board_size

        # look through each row
        for y in range(len(state.board)):
            # look through each field in row
            for x in range(len(state.board[0])):
                # found white piece
                if state.board[y,x] == WHITE:
                    # count white pieces
                    available_white += 1

                    # calculate distance to goal of white piece
                    d = board_size - y - 1
                    # and choose the lowest distance of all pieces
                    if d < distance_white:
                        distance_white = d
                # found black piece
                elif state.board[y,x] == BLACK:
                    # count black pieces
                    available_black += 1

                    # choose the lowest distance to goal of black pieces
                    if y < distance_black:
                        distance_black = y

        if role == "white":
            if distance_white == 0:
                return 100
            if distance_black == 0:
                return -100
            return available_white + (board_size - distance_white)
        else:
            if distance_black == 0:
                return 100
            if distance_white == 0:
                return -100
            return available_black + (board_size - distance_black)

