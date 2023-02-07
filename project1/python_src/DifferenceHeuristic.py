
BLACK, WHITE, EMPTY = "B", "W", " "


class DifferenceHeuristic:

    @staticmethod
    def eval(state):
        distance_black = DifferenceHeuristic.index_2d(state.board, BLACK)
        distance_white = DifferenceHeuristic.index_2d(state.board[::-1], WHITE)
        if distance_black == 0:
            return -100
        if distance_white == 0:
            return 100
        return distance_black * 10

    @staticmethod
    def index_2d(data, search):
        for i in range(len(data)):
            if search in data[i]:
                return i
        raise ValueError("{!r} is not in list".format(search))

