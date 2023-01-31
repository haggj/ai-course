import random
from agent import RandomAgent
from environment import Environment

class MyAgent(RandomAgent):
    def __init__(self):
        self.role = None
        self.play_clock = None
        self.my_turn = False
        self.width = 0
        self.height = 0
        self.env = None
        self.last_move = None

    # start() is called once before you have to select the first action. Use it to initialize the agent.
    # role is either "white" or "black" and play_clock is the number of seconds after which nextAction must return.
    def start(self, role, width, height, play_clock):
        self.play_clock = play_clock
        self.role = role
        self.my_turn = role != 'white'
        # we will flip my_turn on every call to next_action, so we need to start with False in case
        #  our action is the first
        self.width = width
        self.height = height
        # TODO: add your own initialization code here
        self.env = Environment(width=width, height=height)

    def next_action(self, last_action):
        if last_action:
            if self.my_turn and self.role == 'white' or not self.my_turn and self.role != 'white':
                last_player = 'white'
            else:
                last_player = 'black'
            print("%s moved from %s to %s" % (last_player, str(last_action[0:2]), str(last_action[2:4])))
            # TODO: 1. update your internal world model according to the action that was just executed
            x1, y1, x2, y2 = last_action
            if self.last_move != (x1-1, y1-1, x2-1, y2-1) and self.my_turn:
                print("ERRORRRR +++++++++++++")
            self.env.move(self.env.current_state, (x1-1, y1-1, x2-1, y2-1))
        else:
            print("first move!")

        # update turn (above that line it myTurn is still for the previous state)
        self.my_turn = not self.my_turn
        if self.my_turn:
            # TODO: 2. run alpha-beta search to determine the best move
            x1, y1, x2, y2 = self.get_best_move()
            self.last_move = (x1, y1, x2, y2)
            return "(move " + " ".join(map(str, [x1+1, y1+1, x2+1, y2+1])) + ")"
        else:
            return "noop"

    def get_best_move(self):
        legal_moves = self.env.get_legal_moves(self.env.current_state)
        return random.choice(legal_moves)
