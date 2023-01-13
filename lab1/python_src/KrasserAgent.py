from copy import deepcopy
from enum import IntEnum

from agent import Agent

class Orientation(IntEnum):
    NORTH, EAST, SOUTH, WEST = 0, 1, 2 ,3

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        """ For Debugging """
        return f"Position: ({self.x}, {self.y})"

    def __hash__(self):
        """" to add Position to visited hash """
        return hash(str(self))

    def __eq__(self, other):
        """ Check if Position is Home"""
        return self.x == other.x and self.y == other.y

    def __move__(self, orientation, step=1):
        match orientation:
            case Orientation.NORTH:
                self.y += step
            case Orientation.EAST:
                self.x += step
            case Orientation.SOUTH:
                self.y -= step
            case Orientation.WEST:
                self.x -= step


class UturnPhase(IntEnum):
    NONE, FIRST_TURN, GO = 0, 1, 2


class KrasserAgent(Agent):
    def __init__(self):
        # Used for snake
        self.uturn = UturnPhase.NONE
        self.old_orientation = Orientation.NORTH

        self.position = Point()
        self.home = Point()
        self.orientation = Orientation.SOUTH
        self.turned_on = False
        self.visited = {self.home}
        self.bump_counter = 0
        self.go_home = False

    # this method is called on the start of the new environment
    def start(self):
        print("start called")
        self.__init__()
        return

    # this method is called when the environment has reached a terminal state
    # override it to reset the agent
    def cleanup(self, percepts):
        print("cleanup called")
        self.orientation = Orientation.SOUTH
        self.turned_on = False
        self.visited = {self.home}
        self.bump_counter = 0
        self.go_home = False

    def turn_on(self):
        self.turned_on = True
        return "TURN_ON"

    def turn_off(self):
        self.turned_on = False
        return "TURN_OFF"

    def turn_right(self):
        self.orientation = (self.orientation + 1) % 4
        return "TURN_RIGHT"

    def turn_left(self):
        self.orientation = (self.orientation - 1) % 4
        return "TURN_LEFT"

    def go(self):
        self.position.__move__(self.orientation)
        self.visited.add(deepcopy(self.position))
        return "GO"

    def undo_move(self):
        self.visited.remove(self.position)
        self.position.__move__(self.orientation, -1)

    def suck(self):
        return "SUCK"

    # this method is called on each time step of the environment
    # it needs to return the action the agent wants to execute as as string
    def next_action(self, percepts):
        print("next_action called")
        if not self.turned_on:
            return self.turn_on()

        if self.go_home == True:
            if self.position.__eq__(self.home):
                print("FOUND HOME")
                return self.turn_off()
            elif self.position.x > 0:
                """ NEED TO MOVE WEST """
                if self.orientation == Orientation.WEST:
                    return self.go()
                elif self.orientation - Orientation.WEST > 0:
                    return self.turn_left()
                else:
                    return self.turn_right()
            elif self.position.x < 0:
                """ NEED TO MOVE EAST """
                if self.orientation == Orientation.EAST:
                    return self.go()
                elif self.orientation - Orientation.EAST > 0:
                    return self.turn_left()
                else:
                    return self.turn_right()
            elif self.position.x == 0 and self.position.y > 0:
                """ NEED TO MOVE SOUTH """
                if self.orientation == Orientation.SOUTH:
                    return self.go()
                elif self.orientation - Orientation.SOUTH > 0:
                    return self.turn_left()
                else:
                    return self.turn_right()
            elif self.position.x == 0 and self.position.y < 0:
                """ NEED TO MOVE NORTH """
                if self.orientation == Orientation.NORTH:
                    return self.go()
                elif self.orientation - Orientation.NORTH > 0:
                    return self.turn_left()
                else:
                    return self.turn_right()

        if "BUMP" in percepts and self.bump_counter < 2:
            # Initialization mode
            self.undo_move()
            if self.bump_counter < 2:
                self.bump_counter += 1
            return self.turn_right()

        if "BUMP" in percepts and self.bump_counter == 2:
            # Snake mode
            self.undo_move()
            if self.uturn == UturnPhase.GO:
                self.go_home = True
            self.old_orientation = self.orientation
            self.uturn = UturnPhase.FIRST_TURN
            if self.old_orientation == Orientation.NORTH or self.old_orientation == Orientation.EAST:
                return self.turn_right()
            return self.turn_left()

        if "DIRT" in percepts:
            return self.suck()

        if self.uturn == UturnPhase.FIRST_TURN:
            self.uturn = UturnPhase.GO
            return self.go()

        if self.uturn == UturnPhase.GO:
            self.uturn = UturnPhase.NONE
            if self.old_orientation == Orientation.NORTH or self.old_orientation == Orientation.EAST:
                return self.turn_right()
            return self.turn_left()

        return self.go()