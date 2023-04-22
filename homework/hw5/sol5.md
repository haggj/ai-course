# Homework 5 – Artificial Intelligence

# Task 1 - Logic

| #   | Inference Rule                 | Inferred Sentance         |
|-----|--------------------------------|---------------------------|
| 1-9 | from knowledge base            |                           |
| 10  | rule 2 with sentences 6 and 9  | $\lnot (EF \land SF)$     |
| 11  | rule 12 with sentence 10       | $\lnot EF \lor \lnot SF$  |
| 12  | rule 11 with sentence 11       | $\lnot SF \lor \lnot EF$  |
| 13  | rule 14 with sentence 8        | $\lnot \lnot SF$  |
| 14  | rule 6 with sentences 12 and 13* | $\lnot EF$                |
| 15  | rule 2 with sentences 4 and 14 | $\lnot TF$                |
| 16  | rule 6 with sentences 1 and 15 | $TJ$                      |

*for rule 6 to apply one need to substitute 
$\alpha=\lnot SF$ and 
$\beta=\lnot EF$:

$\{\alpha \lor \beta, \lnot \alpha\} \vdash \beta$

$\{\lnot SF \lor \lnot EF, \lnot \lnot SF \} \vdash \lnot EF$

Thus, the trainer John is the thief.


# Task 2 - STRIPS Planning

## 2.1

### The robot can only be at one place.
A exclusive OR is required to express the fact, that the robot can be either in room 1 or in room 2 but not in the same room at the same time:

$(at(robot,1) \lor at(robot,2)) \land \lnot (at(robot,1)\land at(robot,2))$

### If the robot holds something, its hand is not empty and vice versa.

$(\exists x)Holding(robot, x) \implies \lnot Handempty$

This is equivalent to:

$Handempty \implies \lnot (\exists x) Holding(robot, x)$

### An object that is held by the robot is nowhere else.
If the robot is holding an item, there is no valid `at` proposition for this item.

$(\forall x)Holding(robot, x): \lnot(\exists y) at(x,y)$


## 2.2 Branching factors


An upper bound for the branching factor of a **forward search** is given by the maximum number of actions applicable in a state. Given a state, the robot might perform one of the following actions:
- go to the other room (`GotoRoom`) -> maximum one action
- pick up any key (`PickUp`) -> maximum two actions
- drop a  key (`Drop`) -> maximum one action
- lock a door (`Lock`) -> maximum one action
- unlock a door (`Unlock`) -> maximum one action

The upper bound for the branching factor is thus `6` when using forward search.

The branching factor of **backward search** depends on the concrete implementation. For example, if we add a new node for each possible action given a certain goal, the branching factor is assumed to be equal to the branching factor of the forward search.
However, if we only consider the action with the least constraining precondition, the lower bound of the branching factor is one. This is, because only the node with the least constraining precondition will be inserted/considered in the next iteration. Please note, that the computation of this action requires that the goal regression for all applicable actions are computed.

In general, there are more actions relevant to a goal than there are actions applicable to a state. Thus, the branching factor is assumed to be smaller using backward search.

## 2.3 Additional actions

The upper bound for the branching factor for **forward search** increases by $3$ because the robot has more actions available in each state.

The lower bound for the branching factor of **backward search** does not change, assuming that the implemented algorithm only considers the action with the least constraining precondition. At the same time, the computation of the goal regression becomes more complex since more actions must be considered to compute the action with the least constraining precondition.

## 2.4 Backward search

The following is the result of my backward search:

Initial goal:
$Locked(1) \land Locked(2) \land At(key(1), 1) \land At(key(2),1)$

Action: $Drop(key(2), 1)$

$\implies$

Regressed goal: 
$At(robot, 1) \land Holding(robot, key(2)) \land Locked(1) \land Locked(2) \land At(key(1), 1)$

Action: $GoToRoom(2,1)$

$\implies$

Regressed goal: 
$At(robot, 2) \land Holding(robot, key(2)) \land Locked(1) \land Locked(2) \land At(key(1), 1)$

Action: $Lock(2)$

$\implies$

Regressed goal: 
$At(robot,2) \land Holding(robot, key(2)) \land Locked(1) \land At(key(1), 1)$

Action: $GoToRoom(1,2)$

$\implies$

Regressed goal:
$At(robot,1) \land Holding(robot, key(2)) \land Locked(1) \land At(key(1), 1)$

Action: $Pickup(key(2),1)$

$\implies$

Regressed goal: 
$At(robot,1) \land At(key(2),1) \land Handempty \land Locked(1) \land At(key(1), 1)$

Action: $Drop(key(1),1)$

$\implies$

Regressed goal:$At(robot,1) \land Holding(robot, key(1)) \land At(key(2),1)  \land Locked(1)$

Action: $Lock(1)$

$\implies$

Regressed goal: $At(robot,1) \land Holding(robot, key(1)) \land At(key(2),1)$

Action: $PickUp(key(1), 1)$

$\implies$

Regressed goal: $At(robot,1) \land At(key(1),1) \land Handempty \land At(key(2),1)$

This regressed goal is satisfied in the initial state.


## 2.5 Best-First Search
Best-First Search yields an optimal result. Since the cost for each action is one and the optimal path has length $8$, the costs for the resulting path is $8$.