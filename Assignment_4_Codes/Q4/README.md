# Cryptarithm Solver (CSP Assignment)

This project solves a classic **Cryptarithm Puzzle** using a **Constraint Satisfaction Problem (CSP)** approach in Python.

### Problem Solved:

```
  TWO
+ TWO
------
 FOUR
```

Each letter represents a unique digit (0–9), and the goal is to find a valid assignment such that the equation holds true.

---

## 📁 Project Structure

```
.
├── Q4.py
```

---

## 🚀 How It Works

The solver uses a **brute-force CSP approach** with constraints:

### Variables

* Letters: `T, W, O, F, U, R`

### Domain

* Digits: `0–9`

### Constraints

1. Each letter must map to a **unique digit**
2. **No leading zeros**:

   * `T ≠ 0`
   * `F ≠ 0`
3. Arithmetic must satisfy:

   ```
   TWO + TWO = FOUR
   ```

---

## 🧠 Algorithm Used

### 1. Permutation-Based Search

* Generates all possible assignments of digits to letters
* Uses `itertools.permutations` for exhaustive search

### 2. Constraint Checking (Column-wise)

Instead of computing full numbers immediately, the program checks constraints **digit by digit**:

* Ones place:
  `O + O → R (carry C1)`
* Tens place:
  `W + W + C1 → U (carry C2)`
* Hundreds place:
  `T + T + C2 → O (carry C3)`
* Thousands place:
  `C3 → F`

This reduces unnecessary computations and improves efficiency.

---

## ▶️ How to Run

```bash
python Q4.py
```

---

## 📊 Output

* Displays all valid solutions (if any)
* Shows:

  * Letter-to-digit mapping
  * Formatted arithmetic result

Example:

```
Solution 1: {'T': ..., 'W': ..., ...}

  TWO
+ TWO
------
 FOUR
```

---

## 📦 Requirements

* Python 3
* No external libraries required (only `itertools`)

---

## 📌 Notes

* The program ensures correctness using **column-wise validation with carry handling**
* Efficient pruning avoids checking invalid full-number combinations
* Works specifically for this cryptarithm but can be extended to others

---

## ✍️ Assignment Info

This project was created as part of an academic assignment to demonstrate:

* CSP formulation of cryptarithm problems
* Constraint-based pruning
* Search using permutations
* Logical decomposition of arithmetic constraints

---
