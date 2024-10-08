import curses
import math
from util import Direction, Orientation


class ConsoleView(object):

    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.scrollok(1)
        self.stdscr.idlok(1)
        self.stdscr.syncok(1)
        curses.setupterm()

    def display_loaded_grid(self, grid, height, width):
        """Display loaded game board and wait for user response to solve the puzzle."""
        self.display_grid(grid, height, width)

        # # Wait for user input
        # self.stdscr.addstr('\n')
        # self.stdscr.addstr('\n')
        # self.stdscr.addstr('Press any key to find solution. \n')
        # self.stdscr.getch()

    def display_grid(self, grid, height, width):
        """Display the loaded game board."""
        self.stdscr.clear()

        # Display game board
        self.stdscr.addstr("The Puzzle: \n", curses.A_BOLD)
        self.stdscr.addstr("\n")
        for row in range(height):
            for column in range(width):
                vehicle = grid[column][row]
                if vehicle:
                    self.stdscr.addstr("%s " % vehicle.get_name())
                else:
                    self.stdscr.addstr(". ")

                if column == width - 1:
                    self.stdscr.addstr("\n")
        self.stdscr.refresh()

    def display_statistics(self, amount_moves="--", time_delta="--"):
        """Display the statistics of the solving process."""
        print("\n")
        print("\n")
        print("The Statistics: \n", curses.A_BOLD)
        print("\n")

        print("Amount of Moves: %s \n" % amount_moves)
        print("Time Passed: %.3f seconds\n" % time_delta)

    def display_solution(self, solution):
        """Display the moves to solve the puzzle."""
        print("\n")
        print("\n")

        if solution:
            # Convert moves to a user friendly format and display them
            print("The Solution: \n", curses.A_BOLD)
            print("\n")

            solution_size = len(solution)
            items_per_row = math.ceil(solution_size / 4)
            for row_index in range(items_per_row):
                collection = []
                for index in range(4):
                    limit = (index * (items_per_row + 1)) + row_index
                    if limit < solution_size:
                        collection.append(limit)

                for column_index, move in enumerate(solution[i] for i in collection):
                    vehicle = move[0]
                    direction = move[1]
                    direction_name = ""
                    if vehicle.get_orientation() == Orientation.HORIZONTAL and direction == Direction.FORWARD:
                        direction_name = "Right"

                    if vehicle.get_orientation() == Orientation.HORIZONTAL and direction == Direction.BACKWARD:
                        direction_name = "Left"

                    if vehicle.get_orientation() == Orientation.VERTICAL and direction == Direction.FORWARD:
                        direction_name = "Down"

                    if vehicle.get_orientation() == Orientation.VERTICAL and direction == Direction.BACKWARD:
                        direction_name = "Up"

                    display_text = "%02d: %s -> %s " % (collection[column_index] + 1, vehicle.get_name(), direction_name)
                    print(display_text)
                    print(" " * (20 - len(display_text)))

                    if column_index == len(collection) - 1:
                        print("\n")
        else:
            print("This puzzle is unsolvable. Even for me! :( \n")
