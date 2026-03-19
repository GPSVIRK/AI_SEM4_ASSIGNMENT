# A* Battlefield Pathfinder (Python)

This project uses the **A* algorithm** to find the shortest path on a grid with obstacles.

---

## Features

* Generates a grid with obstacles
* Finds shortest path using A*
* Supports 8-direction movement
* Displays the path and grid
* Shows performance metrics

---

## How It Works

* The grid is a 40 × 40 map
* Obstacles are randomly placed
* A* uses a heuristic to find the shortest path efficiently
* The path is shown from start (S) to goal (G)

---

## Run the Code

```bash
python filename.py
```

---

## Input

* Choose obstacle density: `low`, `medium`, or `high`
* Enter start and goal positions in format:

```id="2dzte1"
row,col
```

Example:

```id="f39x9c"
0,0
39,39
```

---

## Output

* Grid with path:

  * `S` = Start
  * `G` = Goal
  * `@` = Path
  * `#` = Obstacle
  * `.` = Free space

* Measures of Effectiveness:

  * Path length
  * Nodes expanded
  * Time taken

---

## Assumptions

* Grid size is fixed (40 × 40)
* Movement cost is constant
* No negative weights

---

## Summary

This project demonstrates how A* algorithm efficiently finds the shortest path in a grid with obstacles.
