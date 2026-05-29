# Implementation of Minimax Search, Alpha-Beta Search, Heuristic Alpha-Beta Search and Monte-Carlo Tree Search

## Objective

The objective of this project is to implement and compare four popular game-tree search algorithms used in Artificial Intelligence:

1. Minimax Search
2. Alpha-Beta Pruning
3. Heuristic Alpha-Beta Search
4. Monte-Carlo Tree Search (MCTS)

A Tic-Tac-Toe game environment is used to demonstrate the correctness and behavior of each algorithm.

---

# Problem Description

Tic-Tac-Toe is a two-player zero-sum game played on a 3×3 board.

- Player X attempts to maximize the utility.
- Player O attempts to minimize the utility.
- A player wins by placing three of their symbols in a row, column, or diagonal.
- If the board is completely filled and no player wins, the game ends in a draw.

Since Tic-Tac-Toe has a finite state space and deterministic actions, it serves as a suitable test environment for adversarial search algorithms.

---

# Algorithms Implemented

## 1. Minimax Search

### Overview

Minimax is a recursive adversarial search algorithm used in two-player zero-sum games.

The algorithm assumes:

- Both players play optimally.
- The maximizing player attempts to maximize the utility value.
- The minimizing player attempts to minimize the utility value.

The algorithm recursively explores the game tree until terminal states are reached.

### Utility Function

For terminal states:

| State | Utility |
|---------|---------|
| X wins | +1 |
| O wins | -1 |
| Draw | 0 |

### Working

1. Generate all legal moves.
2. Recursively evaluate resulting states.
3. Choose the move with maximum utility for X.
4. Choose the move with minimum utility for O.
5. Propagate utilities back to the root.

### Advantages

- Produces optimal decisions.
- Guarantees best move if both players play optimally.

### Disadvantages

- Explores a large number of states.
- Computationally expensive for deep game trees.

### Time Complexity

O(bᵈ)

where:

- b = branching factor
- d = depth of game tree

---

## 2. Alpha-Beta Search

### Overview

Alpha-Beta Search is an optimization of Minimax.

It eliminates branches that cannot influence the final decision.

### Definitions

Alpha (α):
- Best value found so far for the maximizing player.

Beta (β):
- Best value found so far for the minimizing player.

### Pruning Condition

A branch is pruned when:

α ≥ β

This indicates that the current branch cannot improve the final decision.

### Working

1. Start with α = -∞ and β = +∞.
2. Traverse the game tree.
3. Update α and β during exploration.
4. Prune branches when α ≥ β.
5. Return the same optimal move as Minimax.

### Advantages

- Produces identical results to Minimax.
- Explores significantly fewer nodes.

### Disadvantages

- Performance depends on move ordering.

### Time Complexity

Worst Case:

O(bᵈ)

Best Case:

O(b^(d/2))

---

## 3. Heuristic Alpha-Beta Search

### Overview

For large game trees it is often impossible to search until terminal states.

A depth-limited Alpha-Beta Search is therefore used.

When the depth limit is reached, a heuristic evaluation function estimates the quality of the position.

### Heuristic Evaluation Function

The implemented heuristic uses:

- Two X symbols and one empty cell → +10
- One X symbol and two empty cells → +1
- Two O symbols and one empty cell → -10
- One O symbol and two empty cells → -1

Terminal positions receive:

| State | Score |
|---------|---------|
| X wins | +100 |
| O wins | -100 |

### Working

1. Search only up to a fixed depth.
2. Evaluate non-terminal leaf nodes using the heuristic.
3. Use Alpha-Beta pruning during search.
4. Select the move with the highest estimated value.

### Advantages

- Faster than full Minimax.
- Suitable for larger games.

### Disadvantages

- Quality depends on heuristic design.
- Does not guarantee optimal play.

### Time Complexity

O(bᵐ)

where:

- m = search depth limit

---

## 4. Monte-Carlo Tree Search (MCTS)

### Overview

Monte-Carlo Tree Search estimates the strength of moves by performing random simulations.

Unlike Minimax, MCTS does not require exhaustive search.

### Four Phases of MCTS

#### 1. Selection

Starting from the root node, repeatedly select the most promising child using the UCT formula:

UCT = (Wins / Visits) + C * √(ln(Parent Visits) / Visits)

where:

- Wins = successful simulations
- Visits = number of times node was visited
- C = exploration constant

---

#### 2. Expansion

Add one unexplored child node to the search tree.

---

#### 3. Simulation

Play random moves until the game reaches a terminal state.

---

#### 4. Backpropagation

Update statistics for all nodes visited during the simulation.

---

### Advantages

- Handles large search spaces efficiently.
- Does not require handcrafted evaluation functions.
- Widely used in modern game-playing systems.

### Disadvantages

- Results may vary due to randomness.
- Requires many simulations for strong performance.

### Time Complexity

Approximately:

O(Number of Simulations)

per move decision.

---

# Program Structure

search_algorithms.py

Contains:

## TicTacToe Class

Provides:

- Board representation
- Move generation
- State cloning
- Winner detection
- Terminal state checking

---

## Minimax Functions

- minimax()
- minimax_best_move()

---

## Alpha-Beta Functions

- alpha_beta()
- alpha_beta_best_move()

---

## Heuristic Search Functions

- heuristic_evaluation()
- heuristic_alpha_beta()
- heuristic_best_move()

---

## Monte-Carlo Tree Search

### Class

- MCTSNode

### Functions

- rollout()
- mcts()

---

# Test Cases

## Test Case 1

Board:

X O X
_ O _
_ _ _

Current Player: X

Expected Behavior:

- Minimax should select the optimal move.
- Alpha-Beta should return the same move as Minimax.
- Heuristic Alpha-Beta should return a similar move.
- MCTS should converge to the same move after sufficient simulations.

---

## Test Case 2

Empty Board

Expected Behavior:

- All algorithms should select a strong opening move.
- MCTS may vary slightly due to random exploration.

---

## Test Case 3

Near Endgame Position

Board:

X X _
O O _
_ _ _

Current Player: X

Expected Behavior:

- Algorithms should identify the immediate winning move.

---

# Sample Output

Current Board:

X O X
_ O _
_ _ _

Minimax Move: 7

Alpha-Beta Move: 7

Heuristic Alpha-Beta Move: 7

MCTS Move: 7

---

# Correctness Verification

Correctness was verified by:

1. Comparing Alpha-Beta results with Minimax.
2. Testing winning positions.
3. Testing blocking positions.
4. Testing draw positions.
5. Running Monte-Carlo simulations with large iteration counts and observing convergence toward the Minimax solution.

---

# Conclusion

This project successfully implements four important AI search techniques.

The results demonstrate:

- Minimax guarantees optimal play.
- Alpha-Beta achieves the same optimal decisions with fewer node evaluations.
- Heuristic Alpha-Beta enables depth-limited search using evaluation functions.
- Monte-Carlo Tree Search provides an alternative simulation-based approach suitable for large game trees.

These algorithms form the foundation of many modern game-playing and decision-making systems used in Artificial Intelligence.
