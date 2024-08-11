import curses
import math
from util import Direction, Orientation
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation


class GUIView:
    """GUI View class."""

    def plot_board(self, grid, ax, i=None, moves_count=None, possible_moves=None):
        ax.clear()
        ax.set_xlim(0, len(grid[0]))
        ax.set_ylim(0, len(grid))
        ax.set_xticks(range(len(grid[0]) + 1))
        ax.set_yticks(range(len(grid) + 1))
        ax.grid(True)
        ax.invert_yaxis()

        # Draw the board and vehicles
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 0:
                    color = "white"
                else:
                    if cell.type == "broken_down":
                        color = "black"
                    else:
                        color = cell.color
                ax.add_patch(patches.Rectangle((i, j), 1, 1, edgecolor="black", facecolor=color))

        # Draw arrows for possible moves
        if possible_moves:
            for state in possible_moves:
                vehicle = state[0][0][0]
                direction = state[0][0][1]
                orientation = vehicle.get_orientation()
                x_start, y_start = vehicle.start.values()
                x_end, y_end = vehicle.end.values()
                if orientation == Orientation.HORIZONTAL:
                    if direction == Direction.FORWARD:
                        arrow = patches.Arrow(x_end + 0.5, y_end + 0.5, 1, 0, facecolor="red", edgecolor="red")
                    if direction == Direction.BACKWARD:
                        arrow = patches.Arrow(x_start + 0.5, y_start + 0.5, -1, 0, facecolor="red", edgecolor="red")
                if orientation == Orientation.VERTICAL:
                    if direction == Direction.FORWARD:
                        arrow = patches.Arrow(x_end + 0.5, y_end + 0.5, 0, 1, facecolor="red", edgecolor="red")
                    if direction == Direction.BACKWARD:
                        arrow = patches.Arrow(x_start + 0.5, y_start + 0.5, 0, -1, facecolor="red", edgecolor="red")
                ax.add_patch(arrow)

        if i and moves_count:
            ax.text(0.5, 1.05, f"Move: {i + 1}/{moves_count}", transform=ax.transAxes, ha="center")

    def show_solution(self, board, grids, possible_moves=None):
        fig, ax = plt.subplots()

        def animate(i):
            self.plot_board(grids[i], ax, i, len(grids), possible_moves[i])
            return ax

        ani = animation.FuncAnimation(fig, animate, frames=len(grids), interval=400)
        plt.show()
        plt.clf()

    def show_board(self, board, possible_moves):
        fig, ax = plt.subplots()
        grid = board.get_grid()
        self.plot_board(grid, ax, possible_moves=possible_moves)
        plt.show()
        plt.clf()

    def show_statistics(self, time_delta, expanded_nodes, amount_moves="--"):
        print("\n")
        print("\n")
        print("Statistics: \n")
        print("Amount of Moves: %s \n" % amount_moves)
        print("Time Passed: %.3f seconds\n" % time_delta)
        print("Expanded Nodes: %s\n" % expanded_nodes)


class ConsoleView(object):

    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.scrollok(1)
        self.stdscr.idlok(1)
        self.stdscr.syncok(1)
        curses.setupterm()

    def show_board(self, board):
        """Display the loaded game board."""
        grid, height, width = board.get_grid(), board.get_height(), board.get_width()
        # self.stdscr.clear()

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

    def show_statistics(self, time_delta, expanded_nodes, amount_moves="--"):
        print("\n")
        print("\n")
        print("Statistics: \n")
        print("Amount of Moves: %s \n" % amount_moves)
        print("Time Passed: %.3f seconds\n" % time_delta)
        print("Expanded Nodes: %s\n" % expanded_nodes)

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
