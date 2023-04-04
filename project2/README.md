# Final Project: Artificial Intelligence
Reykjavik University, T-622-ARTI Artificial Intelligence.

## Introduction

The goal for our project was to implement our own AI algorithm to solve Sudoku puzzles.
A Sudoku can be defined as a Constraint Satisfaction Problem (CSP).
Therefore we implemented a CSP Sudoku solver with using the Google OR Tools library as our benchmark.
With this CSP Sudoku solver we are able to create a Sudoku puzzle with a generic grid size and also are able to solve this puzzle fast.
In the next step we implemented our own algorithm to solve a given Sudoku and tried to be faster than the CSP Solver, which is using the Google library.
This is a Depth First Search (DFS) algorithm. We implemented this DFS algorithm with 4 different versions to improve its performance to solve the Sudoku.
These 4 versions are:
- sorted
- store_legal
- rec.sorted
- rec.store_legal

## Statistics

We also created a script to calculate two statistics about the Sudoku game.

1. The first statistic is a line graph that plots how many numbers of a solved sudoku can be removed while still having a unique solution to this puzzle.
The X axis displays the grid size of the Sudoku and the Y axis the percentage of Numbers that can be removed.

2. The second statistic measures the time each version of the DFS algorithm, as well as the CSP algorithm, takes to solve the same puzzle.
The plotted time is the average of solving 10 different puzzles for each algorithm.
The X axis displays the label of the algorithm and the Y axis the average time to solve a Sudoku of given size

## Usage

```bash
# Run all algorithms on a 9x9 grid
python3 main.py --algorithm all --n 3
# Comparing CSP with the rec.sorted on a 16x16 grid
python3 main.py --algorithm rec.store_legal --n 4
# Run Statisitc 1 for 4x4, 9x9, 16x16 grid and 10 examples
python3 main.py --n 2 3 4 --plot_numbers_removed true --s 10
```

Executing the `main.py` creates first a Sudoku puzzle with a unique solution. Then this puzzle gets solved by the CSP Solver as benchmark and in the following solved by our DFS algorithm, using the version defined by the user input.
It is also possible to create the statistics mentioned above with adding an optional flag to the input arguments.
To run this script execute main.py with following arguments:
* --algorithm (to choose version of DFS algorithm)
  * sorted 
  * store_legal 
  * rec.sorted 
  * rec.store_legal
  * all (execute all versions)
* --n (to set the grid size of the Sudoku)
  * Value: list of numbers
  * Size n = 3 will create a 9x9 Sudoku
* optional: --plot_comparison (to generate the graph of statistic 2)
  * Value: boolean
* optional: --plot_numbers_removed (to generate the graph of statistic 1)
  * Value: boolean
* optional: --s (number of puzzles for average value of statistic 1)
  * Value: number