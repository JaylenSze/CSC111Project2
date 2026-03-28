"""
Main file, where the code runs

"""

from __future__ import annotations
from graph import Graph
from graph import load_wikipedia_graph
from graph import line_graph
from graph import visualize_path
from typing import Optional


def game_runner(solution_mode: bool, hard_mode: bool) -> None:
    """Runs the wikipedia racing game. If solution mode is True then the fastest path
    is highlighted.
    """
    graph = load_wikipedia_graph("links_export.csv")
    graph.prune_graph()
    tup = graph.random_start_end_point()
    current, end = tup[0], tup[1]
    if solution_mode:
        print("SOLUTION MODE")
    if hard_mode:
        print("HARD MODE")
    print("=======================================================================================================")
    print("Starting page: ", current)
    print("Target page: ", end)
    print("=======================================================================================================")
    time = 0
    distances = []
    shortest_time = graph.shortest_path(current, end)[0]
    pages_visited = [current]
    shortest_path = graph.shortest_path_list(current, end)
    if hard_mode:
        print(shortest_time * 2 - time, " Steps Remaining...")
    while current != end:
        output_current_page(current, end)
        length = graph.shortest_path(current, end)[0]
        distances.append(length)
        optimal_page = graph.shortest_path(current, end)[1]
        neighbors = set(graph.get_vertex(current).random_neighbours(6, optimal_page))

        if solution_mode:
            current = get_input(neighbors, optimal_page)
        else:
            current = get_input(neighbors)

        time += 1
        pages_visited.append(current)
        if hard_mode:
            print(shortest_time * 2 - time, " Steps Remaining...")
        if hard_mode and time >= 2 * shortest_time:
            print("You failed :( You had: ", time, " steps")
            output_ending_sequence(shortest_time, pages_visited, shortest_path, distances)
            return

    print("Congratulations! It took you: ", time, " steps")
    output_ending_sequence(shortest_time, pages_visited, shortest_path, distances)


def get_input(s: set[str], optimal_page: Optional[str] = "") -> str:
    """ Display possible actions at this location

    >>> s = {"A", "B", "C", "D"}
    >>> get_input(s, "B")

    """
    print("List of Pages you can visit: ")
    for page in s:
        print(page)
        if page == optimal_page:
            print("^^^ CHOOSE THIS ONE ^^^")

    # Validate choice
    player_choice = input("\nEnter page: ")
    while player_choice not in s:
        print("That was an invalid page; try again.")
        player_choice = input("\nEnter page: ")

    print("=======================================================================================================")
    print(f"You decided to go to: {player_choice}\n")
    return player_choice


def output_ending_sequence(shortest_time: int, pages_visited: list[str],
                           shortest_path: list[str], distances: list[int]):
    """
    Helper function, just prints out information about the game that the user played.
    """
    print("The shortest path time was ", shortest_time, " steps")
    print("Your path was: ")
    for link in pages_visited:
        print("-", link)
    visualize_path(pages_visited)
    print("The optimal path was: ")
    for link in shortest_path:
        print("-", link)
    visualize_path(shortest_path)
    line_graph(distances)


def output_current_page(current_page: str, target_page: str):
    """
    Helper function, just prints out current page and target page.
    """
    print("Current page: ", current_page)
    print("Target page: ", target_page)
    print("=======================================================================================================")


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # increases the running time of the functions/methods.
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()
    #
    # import doctest
    # doctest.testmod()

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['static_type_checker'],
    #     'extra-imports': ['csv', 'networkx'],
    #     'allowed-io': ['load_review_graph'],
    #     'max-nested-blocks': 4
    # })
    # game_runner(True, False)
    # game_runner(True, True)
    game_runner(False, True)

