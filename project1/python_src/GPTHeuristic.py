
BLACK, WHITE, EMPTY = "B", "W", " "


class GPTHeuristic:

    @staticmethod
    def eval(state):
        player = "W"
        h = 0
        h_factor = 1 if player == 'W' else -1
        for i in range(len(state.board)):
            for j in range(len(state.board[0])):
                if state.board[i][j] == player:
                    # Check if piece can move towards opponent's side
                    if (player == 'W' and i > 0 and state.board[i-1][j] == ' ') or (player == 'B' and i < len(state.board) - 1 and state.board[i+1][j] == ' '):
                        h += h_factor
                    # Check if piece can capture opponent's piece
                    if j > 0 and i > 0 and state.board[i-1][j-1] != player and state.board[i-1][j-1] != ' ':
                        h += h_factor * 2
                    if j < len(state.board[0]) - 1 and i > 0 and state.board[i-1][j+1] != player and state.board[i-1][j+1] != ' ':
                        h += h_factor * 2
                    if j > 0 and i < len(state.board) - 1 and state.board[i+1][j-1] != player and state.board[i+1][j-1] != ' ':
                        h += h_factor * 2
                    if j < len(state.board[0]) - 1 and i < len(state.board) - 1 and state.board[i+1][j+1] != player and state.board[i+1][j+1] != ' ':
                        h += h_factor * 2
                elif state.board[i][j] != ' ':
                    # Check if opponent's piece can move towards player's side
                    if (player == 'W' and i < len(state.board) - 1 and state.board[i+1][j] == ' ') or (player == 'B' and i > 0 and state.board[i-1][j] == ' '):
                        h -= h_factor
                    # Check if opponent's piece can be captured by player's pieces
                    if j > 0 and i > 0 and state.board[i-1][j-1] == player:
                        h -= h_factor * 2
                    if j < len(state.board[0]) - 1 and i > 0 and state.board[i-1][j+1] == player:
                        h -= h_factor * 2
                    if j > 0 and i < len(state.board) - 1 and state.board[i+1][j-1] == player:
                        h -= h_factor * 2
                    if j < len(state.board[0]) - 1 and i < len(state.board) - 1 and state.board[i+1][j+1] == player:
                        h -= h_factor * 2
        return h


    @staticmethod
    def index_2d(data, search):
        for i in range(len(data)):
            if search in data[i]:
                return i
        raise ValueError("{!r} is not in list".format(search))

