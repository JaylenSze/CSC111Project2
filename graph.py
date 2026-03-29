"""CSC111 Winter 2026 Project 2

Instructions (READ THIS FIRST!)
===============================
This Python module contains the graph and vertex classes along with a lot of the
functions used for the project.

Copyright and Usage Information
===============================
This file is Copyright (c) 2026 Jaylen, Sheena, Thomas, Ivans
"""

from __future__ import annotations
import random
from typing import Any
import csv
from collections import deque
import networkx as nx  # Used for visualizing graphs (by convention, referred to as "nx")
import matplotlib.pyplot as plt


class _Vertex:
    """A vertex in the graph that represents a Wikipedia page.

    Instance Attributes:
       - page_name: The name of the Wikipedia page this node represents.
       - neighbours: Article pages that can be navigated to directly from this current Wikipedia page.

    Representation Invariants:
       - self not in self.neighbours
       - self.page_name != ""
       - all(isinstance(v, _Vertex) for v in self.neighbours)
       - self.page_name is the name of a valid wikipedia page
       - the wikipedia that self.page_name represents links to all pages represented by vertices in self.neighbours
    """
    page_name: str
    neighbours: set[_Vertex]

    def __init__(self, page_name: str) -> None:
        """Initialize a new vertex with the given page_name. Initialized with no neighbours.

        Preconditions:
           - page_name is the name of a valid wikipedia page
        """
        self.page_name = page_name
        self.neighbours = set()

    def random_neighbours(self, num_neighbours: int, include: str) -> list[str]:
        """ Returns a sorted list of length num_neighbours. Elements of the list are the names of randomly
        chosen vertices that are neighbours to self. The returned list will have include as an element

        If the length of self.neighbours is less than num_neighbors, it will return a sorted list of the names of
        all neighbouring vertices.

        Preconditions:
            - len(self.neighbours) > 0
            - include in [x.page_name for x in self.neighbours]
        """
        n_list = [x.page_name for x in self.neighbours]
        len_list = min(len(n_list), num_neighbours)
        final_list = random.sample(n_list, len_list)
        if include not in final_list:
            index = random.randint(0, len(final_list) - 1)
            final_list.pop()
            final_list.insert(index, include)
        return sorted(final_list)


class Graph:
    """A graph used to represent a wikipedia page network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the articles contained in this graph.
    #         Maps item to _Vertex object.

    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add an article with a given name to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
           - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]
            v1.neighbours.add(v2)
        else:
            raise ValueError

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.page_name for neighbour in v.neighbours}
        else:
            raise ValueError

    def random_start_end_point(self) -> tuple[str, str]:
        """ Chooses a random starting article to begin with and a random article
        to finish on to complete the game
        Preconditions:
            - len(self._vertices) >= 2
        """

        items = list(self._vertices.keys())
        start = random.choice(items)
        end = random.choice(items)

        while start == end:
            end = random.choice(items)

        return start, end

    def shortest_path(self, start: Any, end: Any) -> tuple[int, Any]:
        """
        Returns length of shortest path as well as the first page on this path. Uses Breadth First Search (BFS)
        to find the shortest path, along with a previous array to store the path.

        Preconditions:
            - start in self._vertices
            - end in self._vertices
            - start != end

        >>> graph = Graph()
        >>> graph.add_vertex(1)
        >>> graph.add_vertex(2)
        >>> graph.add_vertex(3)
        >>> graph.add_vertex(4)
        >>> graph.add_vertex(5)
        >>> graph.add_edge(1, 2)
        >>> graph.add_edge(2, 3)
        >>> graph.add_edge(3, 4)
        >>> graph.add_edge(4, 5)
        >>> graph.shortest_path(1, 5)
        (4, 2)
        >>> graph.add_edge(1, 4)
        >>> graph.shortest_path(1, 5)
        (2, 4)
        """
        vis = set()
        dis = {}
        queue = deque()
        queue.append(start)
        prev = {}
        vis.add(start)
        dis[start] = 0
        while not len(queue) == 0:
            s = queue.popleft()
            for neighbor in self._vertices[s].neighbours:
                u = neighbor.page_name
                if u not in vis:
                    vis.add(u)
                    dis[u] = dis[s] + 1
                    queue.append(u)
                    prev[u] = s

        first_page = end
        while prev[first_page] != start:
            first_page = prev[first_page]

        return dis[end], first_page

    def shortest_path_list(self, start: Any, end: Any) -> list[Any]:
        """
        Returns a list of pages that represent the shortest path. Uses Breadth First Search (BFS)
        to find the shortest path, along with a previous array to store the path.

        Preconditions:
            - start in self._vertices
            - end in self._vertices
            - start != end

        >>> graph = Graph()
        >>> graph.add_vertex(1)
        >>> graph.add_vertex(2)
        >>> graph.add_vertex(3)
        >>> graph.add_vertex(4)
        >>> graph.add_vertex(5)
        >>> graph.add_edge(1, 2)
        >>> graph.add_edge(2, 3)
        >>> graph.add_edge(3, 4)
        >>> graph.add_edge(4, 5)
        >>> graph.shortest_path_list(1, 5)
        [1, 2, 3, 4, 5]
        >>> graph.add_edge(1, 4)
        >>> graph.shortest_path_list(1, 5)
        [1, 4, 5]
        """
        vis = set()
        dis = {}
        queue = deque()
        queue.append(start)
        prev = {}
        vis.add(start)
        dis[start] = 0
        while not len(queue) == 0:
            s = queue.popleft()
            for neighbor in self._vertices[s].neighbours:
                u = neighbor.page_name
                if u not in vis:
                    vis.add(u)
                    dis[u] = dis[s] + 1
                    queue.append(u)
                    prev[u] = s

        path = [end]
        cur_page = end
        while prev[cur_page] != start:
            cur_page = prev[cur_page]
            path.append(cur_page)
        path.append(start)
        path.reverse()
        return path

    def get_vertex(self, name: str) -> _Vertex:
        """ Returns the vertex in self that has name as its page_name.
        If no such vertex exists, raise ValueError

        Preconditions:
           - name in self._vertices
        """
        if name in self._vertices:
            return self._vertices[name]
        raise ValueError

    def prune_graph(self) -> None:
        """ Removes all the vertices in the graph which have no neighbours.
        Removes them from self._vertices and from
        the set of neighbours of each vertex in the graph
        """
        deleted = set()
        for x in self._vertices:
            if len(self._vertices[x].neighbours) == 0:
                deleted.add(self._vertices[x])
        for x in self._vertices:
            self._vertices[x].neighbours -= deleted
        for x in deleted:
            self._vertices.pop(x.page_name)

    def visualize_graph(self) -> None:
        """Visualizes the graph using networks in which a network is created by
        Each wikipedia page (vertex) is illustrated as a node
        Each edge is shown as a connection between each node
        """
        nx_graph = nx.Graph()

        for page in self._vertices:
            nx_graph.add_node(page)
        for page in self._vertices:
            for neighbour in self._vertices[page].neighbours:
                nx_graph.add_edge(page, neighbour.page_name)
        plt.figure()
        nx.draw(nx_graph, with_labels=True)
        plt.show()

    def visualize_node(self, node: str) -> None:
        """Visualizes the graph using networks in which a network is created by NetworkX
        Each wikipedia page (vertex) is illustrated as a node
        Each edge is shown as a connection between each node
        The graph only includes the node provided, the node's neighbours, and all the neighbours' neighbours
        So it includes 2 layers of neighbours
        """
        nx_graph = nx.Graph()

        vertex = self._vertices[node]
        nx_graph.add_node(node)
        for page in vertex.neighbours:
            nx_graph.add_node(page.page_name)
            nx_graph.add_edge(node, page.page_name)
            for x in page.neighbours:
                nx_graph.add_node(x.page_name)
                nx_graph.add_edge(page.page_name, x.page_name)
        plt.figure()
        nx.draw(nx_graph, with_labels=True)
        plt.show()


def load_wikipedia_graph(wikipedia_file: str) -> Graph:
    """Return a populated Graph of all available articles and links parsed
    from a given CSV file.

    Preconditions:
        - wikipedia_file is a valid path to a CSV file in the correct format
    """
    graph = Graph()
    with open(wikipedia_file, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            page_1 = row[1]
            page_2 = row[2]
            graph.add_vertex(page_1)
            graph.add_vertex(page_2)
            graph.add_edge(page_1, page_2)
    return graph


def line_graph(lengths: list[int]) -> None:
    """Plots a line graph tracking the shortest path length over time.
        The points on the line graph have coordinates (i+1, lengths[i]).

    Preconditions:
        - len(lengths) > 0
    """
    move = []
    for i in range(len(lengths)):
        move.append(i + 1)

    plt.figure()
    plt.plot(move, lengths, marker=".", linestyle="-")
    plt.title("Length of Shortest Path Over Time")
    plt.xlabel("Move Number")
    plt.ylabel("Length of Shortest Path to Target Page")
    plt.xticks(move)
    plt.ylim(0, max(lengths))
    plt.show()


def visualize_path(sequence: list[str], title: str) -> None:
    """Visualizes a specific path sequence using the networkx library.
        Each Wikipedia page in the sequence is illustrated as a node.
        The path taken is shown as directed connections between the nodes.

    Preconditions:
        - len(sequence) >= 2
    """
    nx_graph = nx.Graph()
    for page in sequence:
        nx_graph.add_node(page)

    for i in range(len(sequence) - 1):
        nx_graph.add_edge(sequence[i], sequence[i + 1])
    plt.figure()
    plt.title(title)
    nx.draw(nx_graph, with_labels=True)
    plt.show()


if __name__ == '__main__':

    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()
    #
    import doctest
    doctest.testmod()

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'extra-imports': ['random', 'csv', 'collections', 'networkx', 'matplotlib.pyplot', 'graph'],
    #     'allowed-io': ['load_wikipedia_graph', 'output_current_page',
    #                    'output_ending_sequence', 'get_input', 'game_runner'],
    #     'disable': ['static_type_checker'],
    #     'max-nested-blocks': 4
    # })
