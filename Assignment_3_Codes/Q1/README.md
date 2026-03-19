# Dijkstra on Indian Cities Dataset (C++)

This project implements **Dijkstra’s Algorithm** to find the shortest path between two cities using a dataset of Indian cities and distances.

---

## Features

* Reads graph data from a CSV file
* Uses Dijkstra’s algorithm to find shortest distance
* Prints the path between two cities
* Handles invalid input and bad CSV rows

---

## How It Works

* The cities are stored as a graph using an adjacency list
* A priority queue (min-heap) is used to always pick the closest city
* Distances are updated using relaxation
* The path is reconstructed using a parent map

---

## Build & Run

### Compile

```bash
g++ dijkstraImplementation.cpp -o dijkstra
```

### Run

```bash
./dijkstra
```

---

## Input

Enter start and end cities:

```
Delhi Mumbai
```

---

## Output Example

```
Path from start to end:
Delhi --> Jaipur --> Mumbai --> DONE
Final distance traveled: 1477
```

---

## CSV Format

```
City1,City2,Distance
Delhi,Mumbai,1400
Mumbai,Bangalore,980
```

---

## Assumptions

* All distances are non-negative
* Graph is treated as directed
* Invalid rows in CSV are ignored

---

## Time Complexity

* **O((V + E) log V)** for Dijkstra’s algorithm

---

## Summary

This project demonstrates how Dijkstra’s algorithm can be applied to real-world data to compute shortest paths between cities.

