# D* Lite Battlefield Pathfinder (Python)

This project implements the **D* Lite algorithm** for pathfinding in a dynamic environment where obstacles can move, appear, or disappear.

---

## Features

* Uses **D* Lite algorithm** for dynamic path planning
* Supports moving and changing obstacles
* Real-time visualization using **Pygame**
* Replans path automatically when environment changes
* Displays performance metrics

---

## How It Works

* A 40 × 40 grid represents the environment
* The UGV (robot) moves from start to goal
* Obstacles can:

  * Move
  * Appear
  * Disappear
* D* Lite updates the path efficiently without recomputing from scratch

---

## Controls

* `SPACE` → Move one step
* `A` → Auto-run
* `R` → Reset grid
* Mouse Click → Add/remove obstacle
* `ESC / Q` → Quit

---

## Run the Code

```bash id="9oz8xw"
python filename.py
```

---

## Output

* Grid visualization:

  * Green = UGV
  * Red = Goal
  * Cyan = Path
  * Blue shades = Terrain
  * Orange = Moving obstacles

* Measures of Effectiveness:

  * Steps taken
  * Replans triggered
  * Distance traveled
  * Time taken

---

## Assumptions

* Grid size is fixed (40 × 40)
* Movement is 8-directional
* No negative costs

---

## Summary

This project demonstrates how D* Lite efficiently updates paths in a changing environment, making it suitable for real-time navigation problems.
