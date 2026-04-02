# Sudoku Solver (CSP Assignment)

This project implements a **Sudoku Solver** using **Constraint Satisfaction Problem (CSP)** techniques in Python.

It combines:

* **AC-3 (Arc Consistency)**
* **Backtracking**
* **MRV (Minimum Remaining Values)**
* **LCV (Least Constraining Value)**

---

## 📁 Project Structure

```
.
├── Q3.py
```

---

## 🚀 How It Works

The solver treats Sudoku as a CSP:

* **Variables** → Each cell in the grid
* **Domain** → Values from 1 to 9
* **Constraints** →

  * No repeated values in:

    * Row
    * Column
    * 3×3 subgrid

### Execution Flow

1. Initialize domains for all cells
2. Apply **AC-3** to reduce domains
3. Use **Backtracking** with:

   * **MRV** → choose most constrained variable
   * **LCV** → choose least constraining value
4. Recursively solve until complete

---

## ▶️ How to Run

```bash
python Q3.py
```

---

## 🧪 Test Cases

The program includes **3 built-in test cases**:

1. Easy
2. Medium
3. Hard

For each test case:

* The unsolved Sudoku is displayed
* You press **Enter** to view the solution
* Then proceed to the next test case

---

## 🧠 Algorithms Used

### 1. AC-3 (Arc Consistency)

* Eliminates inconsistent values early
* Improves efficiency before backtracking

### 2. Backtracking Search

* Tries values recursively
* Backtracks when constraints fail

### 3. MRV (Minimum Remaining Values)

* Selects the variable with the fewest legal values

### 4. LCV (Least Constraining Value)

* Chooses values that eliminate the fewest options for neighbors

---

## 📊 Output

* Prints Sudoku grids in a readable format:

  * `.` represents empty cells
* Displays:

  * Original puzzle
  * Solved puzzle

Example flow:

```
===== Test Case 1 =====

Problem:
...

Press Enter to see the solution...

Solution:
...
```

---

## 📦 Requirements

* Python 3
* No external libraries required (uses only built-in modules like `copy` and `collections`)

---

## 📌 Notes

* The solver ensures consistency using AC-3 before attempting backtracking
* Deep copies of domains are used to preserve state during recursion
* Designed to handle varying difficulty levels efficiently

---

## ✍️ Assignment Info

This project was created as part of an academic assignment to demonstrate:

* CSP modeling of Sudoku
* Constraint propagation (AC-3)
* Heuristic-based search (MRV, LCV)
* Efficient problem-solving using AI techniques

---
