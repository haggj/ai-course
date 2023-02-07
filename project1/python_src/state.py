BLACK, WHITE, EMPTY = "B", "W", " "

class State:
    def __init__(self, width, height):
        self.board = [[WHITE] * width if i < 2 else
                    [BLACK] * width if i > height - 3 else 
                    [EMPTY] * width for i in range(height)
                    ]
        self.white_turn = True
        self.width = width

    def __str__(self) -> str:
        dash_count = self.width * 4 - 3
        line = "\n" + "-" * dash_count + "\n"
        return line.join([ " | ".join([cell for cell in row]) for row in self.board[::-1]])

    def __hash__(self):
        # TODO (DONE): modify as needed
        h = 1
        for c in str(self.board)+str(self.white_turn):
            h = 101 * h + ord(c)
        return h

    def index_2d(self, data, search):
        for i in range(len(data)):
            if search in data[i]:
                return i
        raise ValueError("{!r} is not in list".format(search))

    def get_state_value(self, role):
        distance_black = self.index_2d(self.board,BLACK)
        distance_white = self.index_2d(self.board[::-1],WHITE)
        if distance_black == 0:
            if role == "white":
                return -100
            else:
                return 100
        if distance_white == 0:
            if role == "white":
                return 100
            else:
                return -100
        if role == "white":
            return distance_black-distance_white
        else:
            return distance_white-distance_black