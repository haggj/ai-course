
BLACK, WHITE, EMPTY = "B", "W", " "
class Pieces_Progress_2:
    @staticmethod
    def eval(state):
        num_black = 0
        num_white = 0
        distance_black = 99
        distance_white = 99
        for i in range(len(state.board)):
            for field in state.board[i]:
                if field == 'W':
                    num_white += 1
                    d = None
                    if i == 0:
                        d = 7
                    else:
                        d= (-i % (len(state.board) - 1))
                    if distance_white > d:
                        distance_white = d
                elif field == 'B':
                    num_black += 1
                    if distance_black > i:
                        distance_black = i
        if distance_black == 0:
            return -100
        if distance_white == 0:
            return 100
        return distance_black - distance_white + num_white - (2 * num_black)