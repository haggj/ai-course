# Homework 1 – Artificial Intelligence

## 1. Definitions

**1.1 Agent**

An agent has the ability to sense its surroundings using sensors, process the information gathered, and make decisions that influence the environment through the use of actuators.

**1.2. Agent function**

The agent function determines what action the agent performs based on the given state of the environment.

**1.3. Rational agent**

The decision of a rational agent is expected to maximize a certain performance measure.

## 2. Soccer robot

**2.1. PEAS**
- Performance Measure: Win the game, stick to the rules, not hurting opponents
- Environment: Soccer pitch, goals, own team, opponent team, ball, referee 
- Actuators: legs and arms powered by motors, voice output 
- Sensors: Microphone (to hear what others are saying), speaker (to give instructions for other players) camera and sonar sensors (to scan the pitch)

**2.2. Environment description**
- fully vs. partially observable: The environment is **fully observable** because I assume the robot is equipped with sensor that scan the full area all the time.
- deterministic vs. stochastic: The environment is **stochastic** because the current state does not determine the next state (e.g. the robot does not know what actions the other players will perform)
- episodic vs. sequential: The environment ist **sequential** since short-term actions have long-term consequences.
- static vs. dynamic: The environment is **dynamic** because it changes all the time. Thus, the agent must worry about the passage of time.
- discrete vs. continuous: The environment is **continuous** because the robot acts in a continuous environment (e.g. time and space).
- single vs. multi-agent: The environment is **multi-agent** since there are competitive players on the pitch.

## 3. Missionaries problem

**3.1. Search problem**

A state can be encoded by the following means:
- **side1**: a tuple indicating how many cannibals and missionaries are located at side 1. E.g. (2,1) means that there are 2 cannibals and 1 missionary.
- **side2**: a tuple indicating how many cannibals and missionaries are located at side 2
- **boat_position**: indicates the current location fot he boat (0=>side1 and 1=>side2)

A state is encoded as: (side1, side2, boat_position).
The initial state is ((3,3), (0,0), 0) (all entities on side 1, boat on side 1).
The final state is ((0,0), (3,3), 1) (all entities on side 2, boat on side 2).

There are the following actions defined. Each action is a tuple which indicates how many cannibals and missionaries are transported to the other side. Thus, each action changes the current boat_position and the entities placed on both sides of the river. In total there are the following five options:
- (0,2): two missionaries are transported to the other side
- (0,1): one missionary is transported to the other side
- (1,1): one missionary and one cannibal are transported to the other side
- (1,0): one cannibal is transported to the other side
- (2,0): two cannibals are transported to the other side

**3.2. Estimates**
- average branching factor b is probably in the interval [1;2], because in almost every state we can only take a limited set of actions to avoid that the missionaries are eaten by the cannibals.
- depth of the shortest solution is 11, because the following 11 steps are the fastest way to solve the problem:
    - ((3,3), (0,0), 0) take action (2,0)
    - ((1,3), (2,0), 1) take action (1,0)
    - ((2,3), (1,0), 0) take action (2,0)
    - ((0,3), (3,0), 1) take action (1,0)
    - ((1,3), (2,0), 0) take action (0,2)
    - ((1,1), (2,2), 1) take action (1,1)
    - ((2,2), (1,1), 0) take action (0,2)
    - ((2,0), (1,3), 1) take action (1,0)
    - ((3,0), (0,3), 0) take action (2,0)
    - ((1,0), (2,3), 1) take action (1,0)
    - ((2,0), (1,3), 0) take action (2,0)
    - ((0,0), (3,3), 1) which is the final state
- If the number of cannibals and missionaries are fixed on side 1, the leftover entities must be placed on side 2. Thus, the selection of side 1 is enough to find all possible locations of the entities. On side 1, we can either have 3, 2, 1 or 0 cannibals/missionaries. All combinations are possible (4\*4=16). Since the boat can be on both sides, the estimated size of the state space is 16\*2=32.
- The search tree only contains valid states, e.g. states in which the number of cannibals is not bigger than the number of missionaries on both sides. 
The possible distribution of missionaries and cannibals:

|Side 1|Side 2|comment|
|-|-|-|
|3,0|0,3||   
|3,1|0,2|invalid
|3,2|0,1|invalid
|3,3|0,0|
|2,0|1,3|
|2,1|1,2|invalid
|2,2|1,1|
|2,3|1,0|
|1,0|2,3|
|1,1|2,2|
|1,2|2,1|invalid
|1,3|2,0|
|0,0|3,3|
|0,1|3,2|invalid
|0,2|3,1|invalid
|0,3|3,0|

There are 6 invalid distributions and 10 valid distributions.
Since the boat can be on each side of the side, I estimate that there are 2*10=20 valid states in total.

**3.3. Sate space vs search tree**

The state space contains more states than the search tree, because the search tree only contains states which are reachable by the initial state. The search algorithm only explores reachable states. The state space, however, also contains all theoretical possible states based on the chosen representation.

**3.4. Number of reachable states**

I executed a breath-first search. If a invalid state was reached, I stopped the branch. I did not re-visit already seen states. In total, my search yielded 23 states. This is less than the estimated state space, because my search stopped once an invalid state was reached (event though the algorithm could continue to reach even more invalid states). 