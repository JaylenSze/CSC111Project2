"""CSC111 Winter 2026 Project 2

Instructions (READ THIS FIRST!)
===============================
This Python module contains the game_runner function and helper functions, along with
main function that runs the code.

Copyright and Usage Information
===============================
This file is Copyright (c) 2026 Jaylen, Sheena, Thomas, Ivans
"""

from __future__ import annotations
from typing import Optional
from graph import load_wikipedia_graph
from graph import line_graph
from graph import visualize_path


def game_runner(solution_mode: bool, hard_mode: bool, graph_file: str, num_pages: int) -> None:
    """Runs the Wikipedia Racing game based on user settings.

        If solution_mode is True, the fastest path choice is highlighted for the player.
        If hard_mode is True, the player has at most (2 * the shortest path length)
        steps to reach the target end page before losing.
    """
    graph = load_wikipedia_graph(graph_file)
    graph.prune_graph()
    current, end = graph.random_start_end_point()
    start = current
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
        distances.append(graph.shortest_path(current, end)[0])
        optimal_page = graph.shortest_path(current, end)[1]
        neighbors = set(graph.get_vertex(current).random_neighbours(num_pages, optimal_page))

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

    graph.visualize_node(start)


def get_input(s: set[str], optimal_page: Optional[str] = "") -> str:
    """Display possible actions (available links) at the current page and prompt user for selection.

        If optimal_page is provided (and not an empty string), it will be highlighted
        as the recommended choice.

        Preconditions:
            - len(s) > 0
            - optimal_page == "" or optimal_page in s
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
                           shortest_path: list[str], distances: list[int]) -> None:
    """Helper function to print out final statistics and visualizations about the game
        the user just played, including their path compared to the optimal path.

    Preconditions:
        - len(pages_visited) > 0
        - len(shortest_path) > 0
    """
    print("The shortest path time was ", shortest_time, " steps")
    print("Your path was: ")
    for link in pages_visited:
        print("-", link)
    visualize_path(pages_visited, "Your Path")
    print("The optimal path was: ")
    for link in shortest_path:
        print("-", link)
    visualize_path(shortest_path, "Optimal Path")
    line_graph(distances)


def output_current_page(current_page: str, target_page: str) -> None:
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
    #     'extra-imports': ['random', 'csv', 'collections', 'networkx', 'matplotlib.pyplot', 'graph'],
    #     'allowed-io': ['load_wikipedia_graph', 'output_current_page',
    #                    'output_ending_sequence', 'get_input', 'game_runner'],
    #     'disable': ['static_type_checker'],
    #     'max-nested-blocks': 4
    # })
    # SOLUTION MODE UNCOMMENT FOR IT TO RUN
    # game_runner(True, False, 'links_export.csv', 6)

    # SOLUTION AND HARD MODE UNCOMMENT FOR IT TO RUN
    # game_runner(True, True, 'links_export.csv', 6)

    # HARD MODE
    game_runner(False, True, 'links_export.csv', 6)

    # HARD MODE (10 pages display)
    # game_runner(False, True, 'links_export.csv', 10)

    # NO SOLUTION AND NO HARD MODE UNCOMMENT FOR IT TO RUN
    # game_runner(False, False, 'links_export.csv', 6)
