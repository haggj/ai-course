import collections
from queue import PriorityQueue

from environment import Environment


######################

class Heuristics:
    env = None

    # inform the heuristics about the environment, needs to be called before the first call to eval()
    def init(self, env):
        self.env = env

    # return an estimate of the remaining cost of reaching a goal state from state s
    def eval(self, s):
        raise NotImplementedError()


######################

class SimpleHeuristics(Heuristics):

    def eval(self, s):
        h = 0
        # if there is dirt: max of { manhattan distance to dirt + manhattan distance from dirt to home }
        # else manhattan distance to home
        if len(s.dirts) == 0:
            h = self.nb_steps(s.position, self.env.home)
        else:
            for d in s.dirts:
                steps = self.nb_steps(s.position, d) + self.nb_steps(d, self.env.home)
                if (steps > h):
                    h = steps
            h += len(s.dirts)  # sucking up all the dirt
        if s.turned_on:
            h += 1  # to turn off
        return h

    # estimates the number of steps between locations a and b by Manhattan distance
    def nb_steps(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


class KrassereHeuristics(Heuristics):

    def eval(self, s):
        h = 0
        # if there is dirt: max of { manhattan distance to dirt + manhattan distance from dirt to home }
        # else manhattan distance to home
        if len(s.dirts) == 0:
            h = self.nb_steps(s.position, self.env.home)
        else:

            # Finding the closest dirt
            close_dirt = None
            steps_close_dirt = None
            for d in s.dirts:
                steps = self.nb_steps(s.position, d)
                if not steps_close_dirt or steps_close_dirt > steps:
                    steps_close_dirt = steps
                    close_dirt = d

            # Finding the furthest dirt
            far_dirt = None
            steps_far_dirt = None
            for d in s.dirts:
                steps = self.nb_steps(close_dirt, d)
                if not steps_far_dirt or steps_far_dirt < steps:
                    steps_far_dirt = steps
                    far_dirt = d

            h = self.nb_steps(s.position, close_dirt) + self.nb_steps(close_dirt,
                                                                      far_dirt) + self.nb_steps(
                far_dirt, self.env.home)
            h += len(s.dirts)  # sucking up all the dirt

        if s.turned_on:
            h += 1  # to turn off
        return h

    # estimates the number of steps between locations a and b by Manhattan distance
    def nb_steps(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

######################

class SearchAlgorithm:
    heuristics = None

    def __init__(self, heuristics):
        self.heuristics = heuristics

    # searches for a goal state in the given environment, starting in the current state of the environment,
    # stores the resulting plan and keeps track of nb. of node expansions, max. size of the frontier and cost of best solution found
    def do_search(self, env):
        raise NotImplementedError()

    # returns the plan found, the last time do_search() was executed
    def get_plan(self):
        raise NotImplementedError()

    # returns the number of node expansions of the last search that was executed
    def get_nb_node_expansions(self):
        raise NotImplementedError()

    # returns the maximal size of the frontier of the last search that was executed
    def get_max_frontier_size(self):
        raise NotImplementedError()

    # returns the cost of the plan that was found
    def get_plan_cost(self):
        raise NotImplementedError()


######################

# A Node is a tuple of these four items:
#  - value: the evaluation of this node
#  - parent: the parent of the node, or None in case of the root node
#  - state: the state belonging to this node
#  - action: the action that was executed to get to this node (or None in case of the root node)

Node = collections.namedtuple('Node', ['value', 'parent', 'state', 'action'])


######################

class AStarSearch(SearchAlgorithm):
    nb_node_expansions = 0
    max_frontier_size = 0
    goal_node = None

    def __init__(self, heuristic):
        super().__init__(heuristic)

    def do_search(self, env: Environment):
        self.heuristics.init(env)
        self.nb_node_expansions = 0
        self.max_frontier_size = 0
        self.goal_node = None

        # Create a priority queue for the frontier
        frontier = PriorityQueue()

        # Create the start node and add it to the frontier
        start_node = Node(0, None, env.get_current_state(), None)
        frontier.put(start_node)

        # Create a set to keep track of the explored states
        explored = set()

        # Create a dictionary to keep track of states that are in the frontier
        states_in_frontier = {}
        states_in_frontier[start_node.state] = start_node.value

        counter = 0
        #while not frontier.empty():
        while frontier:
            # Get the node with the lowest value from the frontier
            current_node = frontier.get()

            if current_node.state in explored:
                continue

            # Check if the current node is the goal state
            if env.is_goal_state(current_node.state):
                self.goal_node = current_node
                break

            # Mark the current state as explored
            explored.add(current_node.state)

            # Expand the current node and add the resulting nodes to the frontier
            for action in env.get_legal_actions(current_node.state):
                next_state = env.get_next_state(current_node.state, action)

                if next_state not in explored:
                    # Compute the value of the node using the heuristic function
                    cost = env.get_cost(current_node.state, action)
                    value = current_node.value + cost + self.heuristics.eval(next_state)

                    # Check if this state already exits in frontier
                    if next_state in states_in_frontier and value > states_in_frontier[next_state]:
                        # State with less cost already exits
                        continue

                    # Create the new node and add it to the frontier
                    new_node = Node(value, current_node, next_state, action)

                    frontier.put(new_node)
                    states_in_frontier[new_node.state] = new_node.value
                    self.nb_node_expansions += 1
                    self.max_frontier_size = max(self.max_frontier_size, frontier.qsize())
                    if counter == 10000:
                        print(self.heuristics.eval(next_state))
                        counter = 0
                    counter += 1

    def get_plan(self):
        if not self.goal_node:
            return None

        plan = []
        n = self.goal_node
        while n.parent:
            plan.append(n.action)
            n = n.parent

        return plan[::-1]

    def get_nb_node_expansions(self):
        return self.nb_node_expansions

    def get_max_frontier_size(self):
        return self.max_frontier_size

    def get_plan_cost(self):
        if self.goal_node:
            return self.goal_node.value
        else:
            return 0
