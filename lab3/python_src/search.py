import collections
import time
from copy import deepcopy
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

            move_order = [s.position]
            dirt_help_list = list(deepcopy(s.dirts))
            for dirt in s.dirts:
                next_dirt = None
                steps_next_dirt = None
                for d in dirt_help_list:
                    steps = self.nb_steps(move_order[(len(move_order) - 1)], d)
                    if not steps_next_dirt or steps_next_dirt > steps:
                        steps_next_dirt = steps
                        next_dirt = d
                move_order.append(next_dirt)
                dirt_help_list.remove(next_dirt)

            move_order.append(self.env.home)

            total_steps = 0
            for i in range(len(move_order) - 1):
                total_steps += self.nb_steps(move_order[i], move_order[i+1])

            h = total_steps + len(s.dirts)  # sucking up all the dirt

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

Node = collections.namedtuple('Node', ['value', 'costs', 'parent', 'state', 'action'])


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
        start_node = Node(0, 0, None, env.get_current_state(), None)
        frontier.put(start_node)

        # Create a set to keep track of the explored states
        explored = set()

        cached_costs = dict()

        start = time.time()

        while not frontier.empty():
            # Get the node with the lowest value from the frontier
            current_node = frontier.get()

            # Check if the current node is the goal state
            if env.is_goal_state(current_node.state):
                self.goal_node = current_node
                break

            # Mark the current state as explored
            explored.add(current_node.state)

            # Expand the current node and add the resulting nodes to the frontier
            for action in env.get_legal_actions(current_node.state):
                next_state = env.get_next_state(current_node.state, action)

                next_cost_g = current_node.costs + env.get_cost(current_node.state, action)
                next_cost_h = self.heuristics.eval(next_state)
                next_cost_f = next_cost_g + next_cost_h

                if next_state in explored:
                    continue

                if next_state in cached_costs:
                    # state is already in queue, check if we found a better path
                    if cached_costs[next_state].value <= next_cost_f:
                        # detected path is more expensive -> drop
                        continue
                    else:
                        frontier.queue.remove(cached_costs[next_state])

                # Create the new node and add it to the frontier
                new_node = Node(next_cost_f, next_cost_g, current_node, next_state, action)
                frontier.put(new_node)
                cached_costs[new_node.state] = new_node
                self.nb_node_expansions += 1
                if self.nb_node_expansions % 50000 == 0:
                    print(self.nb_node_expansions)
                self.max_frontier_size = max(self.max_frontier_size, frontier.qsize())

        end = time.time()
        print(f"Took {end-start}s to expand {self.nb_node_expansions} nodes.")
        print(f"Maximal frontier size: {self.max_frontier_size}.\n\n\n")


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
