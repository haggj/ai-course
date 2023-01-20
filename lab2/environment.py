from enum import IntEnum
import random
import itertools
import math
import hashlib
import copy

##############

class Orientation(IntEnum):
  NORTH = 0
  EAST = 1
  SOUTH = 2
  WEST = 3

  # this allows things like: Orientation.NORTH + 1 == Orientation.EAST
  def __add__(self, i):
    orientations = list(Orientation)
    return orientations[(int(self) + i) % 4]

  def __sub__(self, i):
    orientations = list(Orientation)
    return orientations[(int(self) - i) % 4]

##############

class State:
  # Note, that you do not necessarily have to use this class if you find a
  # different data structure more useful as state representation.
  _id = None

  # TODO: add other attributes that store necessary information about a state of the environment
  #       Only information that can change over time should be kept here.

  def __init__(self, turned_on=False, position=(0,0), dirts_left=[], orientation=Orientation.NORTH):
  # TODO (DONE): add other attributes that store necessary information about a state of the environment
    self.turned_on = turned_on
    self.position = position
    self.dirts_left  = dirts_left
    self.orientation = orientation

  def __str__(self):
    # TODO (DONE): modify as needed
    return "State(%s, %s, %s, %s)" % (str(self.turned_on), str(self.position), str(self.dirts_left), str(self.orientation))

  def __hash__(self):
    # TODO (DONE): modify as needed
    h = 1
    for c in str(self):
      h = 101 * h  +  ord(c)
    return h

  def __eq__(self, o: 'State'):
    # TODO (DONE): modify as needed
    return hash(self) == hash(o)
    return self.turned_on == o.turned_on and \
           self.position == o.position and \
           self.dirts_left == o.dirts_left and \
           self.orientation == o.orientation

##############

class Environment:
  # TODO: add other attributes that store necessary information about the environment
  #       Information that is independent of the state of the environment should be here.

  def __init__(self, width=5, height=5, nb_dirts=5):
    self._width = width
    self._height = height
    # TODO (DONE): randomly initialize an environment of the given size
    # That is, the starting position, orientation and position of the dirty cells should be (somewhat) random.
    # for example as shown here:
    # generate all possible positions
    self.all_positions = list(itertools.product(range(1, self._width+1), range(1, self._height+1)))
    # randomly choose a home location
    self.home = random.choice(self.all_positions)
    # randomly choose locations for dirt
    self.dirts = random.sample(self.all_positions, nb_dirts)
    self.initial_orientation = random.choice([Orientation.NORTH, Orientation.SOUTH, Orientation.WEST, Orientation.EAST])

  def get_initial_state(self):
    # TODO (DONE): return the initial state of the environment
    # return State(False, position=(0,0), dirts_left=self.dirts, orientation=Orientation.WEST)
    return  State(False, position=self.home, dirts_left=copy.deepcopy(self.dirts), orientation=self.initial_orientation)

  def will_bump(self, state: State):
    if state.orientation == Orientation.NORTH:
      return self._height == state.position[1]
    elif state.orientation == Orientation.SOUTH:
      return 1 == state.position[1]
    elif state.orientation == Orientation.WEST:
      return 1 == state.position[0]    
    else:
      return self._width == state.position[0]

  def get_legal_actions(self, state: State):
    actions = []
    # TODO (DONE): check conditions to avoid useless actions
    if not state.turned_on:
      actions.append("TURN_ON")
    else:
      if state.position == self.home and state.dirts_left == []: # should be only possible when agent has returned home
        actions.append("TURN_OFF")
      if state.position in state.dirts_left: # should be only possible if there is dirt in the current position
        actions.append("SUCK")
      if not self.will_bump(state): # should be only possible when next position is inside the grid (avoid bumping in walls)
        actions.append("GO")
      actions.append("TURN_LEFT")
      actions.append("TURN_RIGHT")
    return actions

  def get_next_state(self, state: State, action):
    # TODO (DONE): add missing actions
    if action == "TURN_ON":
      return State(True,state.position, copy.deepcopy(state.dirts_left), state.orientation)

    elif action == "TURN_OFF":
      return State(False,state.position, copy.deepcopy(state.dirts_left), state.orientation)

    elif action == "SUCK":
      if state.position in state.dirts_left:
        new_dirts = copy.deepcopy(state.dirts_left)
        new_dirts.remove(state.position)
      return State(state.turned_on, state.position, new_dirts, state.orientation)

    elif action == "GO":
      new_position = None
      if state.orientation == Orientation.NORTH:
        new_position = (state.position[0], state.position[1]+1)
      elif state.orientation == Orientation.SOUTH:
        new_position = (state.position[0], state.position[1]-1)
      elif state.orientation == Orientation.WEST:
        new_position = (state.position[0]-1, state.position[1])
      elif state.orientation == Orientation.EAST:
        new_position = (state.position[0]+1, state.position[1])
      return State(state.turned_on, new_position, copy.deepcopy(state.dirts_left), state.orientation) 

    elif action == "TURN_LEFT":
     return State(state.turned_on, state.position, copy.deepcopy(state.dirts_left), state.orientation-1)

    elif action == "TURN_RIGHT":
      return State(state.turned_on, state.position, copy.deepcopy(state.dirts_left), state.orientation+1)

    else:
      raise Exception("Unknown action %s" % str(action))

  def get_cost(self, state: State, action):
    # TODO (DONE): return correct cost of each action
    if action == "TURN_OFF":
      costs = 1 if state.position == self.home else 100
      return costs + 50*len(state.dirts_left)
    if action == "SUCK" and state.position not in state.dirts_left:
      return 5
    return 1

  def is_goal_state(self, state: State):
    # TODO(DONE): correctly implement the goal test
    return not state.turned_on and state.dirts_left == [] and state.position == self.home

##############

def expected_number_of_states(width, height, nb_dirts):
  # TODO (DONE): return a reasonable upper bound on number of possible states
  sum = 0
  for n in range(nb_dirts+1):
    sum += math.factorial(width*height)/math.factorial(width*height-n)
  return 2*width*height*4*sum
