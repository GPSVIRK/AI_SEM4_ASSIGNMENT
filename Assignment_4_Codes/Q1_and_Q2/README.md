# Map Colouring Assignment

This project implements a **Constraint Satisfaction Problem (CSP)** approach to solve the **map colouring problem** using C++, and then visualizes the result using Python.

---

## 📁 Project Structure

```
.
├── images/
│   ├── Australia.svg
│   ├── Telangana.svg
├── Australia.csv
├── Telangana.csv
├── mapColouring.cpp
├── mapColouringVisualiser.py
├── state_district_connections.hpp
├── result.json (generated)
├── Australia_out.svg (generated)
├── Telangana_out.svg (generated)
```

---

## 🚀 How It Works

1. The C++ program:

   * Reads adjacency data from `.csv` files
   * Solves the map colouring problem using **backtracking**
   * Outputs the solution to a `result.json` file

2. The C++ program then automatically:

   * Calls the Python script

3. The Python script:

   * Reads `result.json`
   * Applies colours to the SVG maps
   * Outputs coloured SVG files (`*_out.svg`)

---

## ▶️ How to Run

### 1. Compile the C++ Code

```bash
g++ mapColouring.cpp -o mapColouring
```

### 2. Run the Program

```bash
./mapColouring
```

That’s it — running the C++ executable will:

* Solve the colouring problem
* Generate `result.json`
* Automatically run the Python visualizer
* Produce coloured maps:

  * `Australia_out.svg`
  * `Telangana_out.svg`

---

## 🧠 Algorithm Used

* **Backtracking CSP**
* Heuristic:

  * Chooses the node with the **maximum number of neighbours** (a variation of degree heuristic)
* Uses:

  * Constraint checking via forbidden colour lists

---

## 📦 Requirements

* **C++ Compiler** (g++)
* **Python 3**

No external Python libraries are required (only built-in modules like `xml` and `json` are used).

---

## 📌 Notes

* Make sure all file paths (especially inside the `images/` folder) are correct.
* The Python script is automatically invoked using `system()` in C++.
* If the Python script fails, an error message will be shown.

---

## 📊 Output

* `result.json` → raw colouring data
* `Australia_out.svg` → coloured Australia map
* `Telangana_out.svg` → coloured Telangana map

You can open the `.svg` files in any browser to view the results.

---

## ✍️ Assignment Info

This project was created as part of an academic assignment to demonstrate:

* CSP problem solving
* Backtracking algorithms
* Cross-language integration (C++ + Python)
* Data visualization using SVG

---
