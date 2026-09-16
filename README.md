# CSC111 Project Proposal: Wikipedia Racing

**Authors:** Yuhuan Chen, Sheena Qin, Jaylen Sze, Thomas Tran  
**Date:** September 2026  

---

## Overview & Research Question

* **Game Mechanics:** 
  * Wikipedia racing is a game where players attempt to navigate from a designated starting Wikipedia article to a target article solely by clicking hyperlinked text within each page.
  * A random generator selects the starting and target pages (e.g., navigating from "China" to "Japan").
* **Motivation:**
  * Wikipedia forms a massive, interconnected network of articles.
  * Navigating this web reflects how users explore large information networks under uncertainty and incomplete information at each step.
  * Graph theory naturally models this structure: articles act as nodes, and hyperlinks act as directed edges.
* **Core Research Question:**
  * *How can we model Wikipedia as a graph and compute efficient navigation paths between articles?*
  * In particular, how can graph algorithms (such as shortest-path search) be used to analyze and improve navigation in a Wikipedia Racing setting?

---

## Computational Plan

### Graph Representation & Dataset
* **Graph Modeling:**
  * **Nodes:** Individual Wikipedia articles.
  * **Edges:** Directed hyperlinks between pages (hyperlinks are one-directional by nature).
* **Dataset:**
  * We use a curated subset of Wikipedia: [Wikipedia Link Graph - 15K Pages Dataset on Kaggle](https://www.kaggle.com/datasets/kutayahin/wikipedia-link-graph-15k?select=links_export.csv).
  * Contains page names and directed connections in CSV format.
  * Keeps graph traversal and analysis computationally feasible compared to parsing the full 7+ million English Wikipedia articles.

![Dataset Overview](table.png)

### Key Operations & Algorithms
* **Graph Construction:** Parse the CSV dataset into a directed graph data structure.
* **Data Sanitization:** Filter out hyperlinks pointing to pages not present within the subset.
* **Network Diameter & Max Distance:** Compute the maximum shortest-path distance between reachable node pairs.
* **Shortest Path Computation:** Run shortest-path search algorithms between any given pair of articles and output the optimal trajectory.
* **Progress Tracking:** Evaluate distance metrics at each player step to assess user navigation efficiency.

### Game Simulation & Visualization
* Players receive randomly selected starting and ending Wikipedia articles.
* At each step, the player selects from a subset of outgoing links, guaranteed to include at least one optimal path candidate.
* Navigation performance over time is tracked by measuring the remaining shortest path to the goal at each turn.
* `matplotlib.pyplot` is used to plot navigation curves (e.g., remaining path length vs. turns taken) using standard plotting tools (`plot()`, `xlabel()`, `ylabel()`, `title()`).

---

## References

* The Matplotlib development team. *matplotlib.pyplot.plot*. Matplotlib 3.10.8 documentation. [https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html)
* Wikipedia Editors. (2026, February 26). *Wikiracing*. Wikipedia. [https://en.wikipedia.org/wiki/Wikiracing](https://en.wikipedia.org/wiki/Wikiracing)
* Şahin, K. (2025, November 30). *Wikipedia Link Graph Dataset - 15K Pages*. Kaggle. [https://www.kaggle.com/datasets/kutayahin/wikipedia-link-graph-15k](https://www.kaggle.com/datasets/kutayahin/wikipedia-link-graph-15k)
