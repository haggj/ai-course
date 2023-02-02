from my_agent import MyAgent
from state import State

tested_agent = MyAgent()


class TestAgent:

    def empty_state(self):
        state = State(width=10, height=10)
        # Clear board
        for i in range(10):
            for j in range(10):
                state.board[i][j] = " "
        return state

    def validate_moves(self, agent, expected_moves):

        print(agent.env.current_state)

        # Compute  moves
        moves = agent.env.get_legal_moves(tested_agent.env.current_state)

        # Check if only expected moves are returned
        for tested_field in expected_moves.keys():
            # filter moves for field under test:
            condition = lambda move: move[0] == tested_field[0] and move[1] == tested_field[1]
            print(f"Expected moves for {tested_field}: {expected_moves[tested_field]}")
            print(f"Returned moves for {tested_field}: {list(filter(condition, moves))}\n\n")
            for returned_move in filter(condition, moves):
                if returned_move not in expected_moves[tested_field]:
                    raise Exception(
                        f"Legal move not expected because {returned_move} not in {expected_moves[tested_field]}")
                expected_moves[tested_field].remove(returned_move)

            if expected_moves[tested_field]:
                raise Exception(f"Expected moves not returned: {expected_moves[tested_field]}")

    def test_white_moves(self):
        expected_moves = {}
        state = self.empty_state()

        # Bottom-left corner
        state.board[0][0] = "W"
        state.board[2][1] = "B"
        state.board[1][2] = "B"
        expected_moves[(0,0)] = []

        # Bottom-right corner
        state.board[0][9] = "W"
        state.board[1][8] = "B"
        expected_moves[(9, 0)] = [
            (9, 0, 8, 2), # move
            (9, 0, 8, 1), # beat
            (9, 0, 7, 1), # move
        ]

        # Center
        state.board[5][5] = "W"
        state.board[6][6] = "B"
        state.board[6][4] = "B"
        expected_moves[(5, 5)] = [
            (5, 5, 7, 6),  # move
            (5, 5, 6, 7),  # move
            (5, 5, 4, 7),  # move
            (5, 5, 3, 6),  # move
            (5, 5, 6, 6),  # beat
            (5, 5, 4, 6),  # beat
        ]

        # Assign state to env
        tested_agent.start("white", width=10, height=10, play_clock=10)
        tested_agent.env.current_state = state
        self.validate_moves(tested_agent, expected_moves)

    def test_black_moves(self):
        expected_moves = {}
        state = self.empty_state()

        # Top-right corner
        state.board[9][9] = "B"
        state.board[8][8] = "W"
        expected_moves[(9, 9)] = [
            (9, 9, 8, 7), # move
            (9, 9, 7, 8), # move
            (9, 9, 8, 8), # beat
        ]

        # Top-left corner
        state.board[9][0] = "B"
        state.board[8][1] = "W"
        state.board[7][1] = "W"
        expected_moves[(0,9)]=[
            (0, 9, 2, 8), # move
            (0, 9, 1, 8), # move
        ]

        # Center
        state.board[5][5] = "B"
        state.board[4][4] = "W"
        state.board[4][6] = "W"
        expected_moves[(5, 5)] = [
            (5, 5, 4, 3),  # move
            (5, 5, 3, 4),  # move
            (5, 5, 6, 3),  # move
            (5, 5, 7, 4),  # move
            (5, 5, 4, 4),  # beat
            (5, 5, 6, 4),  # beat
        ]
        # Assign state to env
        state.white_turn = False
        tested_agent.start("black", width=10, height=10, play_clock=10)
        tested_agent.env.current_state = state
        self.validate_moves(tested_agent, expected_moves)