import threading
from copy import deepcopy
from enum import Enum
from util import Direction, Orientation
import util


class Node:
    def __init__(self, state, path, cost):
        self.state = state
        self.path = path
        self.cost = cost


class BoardSolver(object):
    def __init__(self, game_board):
        self.game_board = game_board
        # self.console_view = console_view
        self.solution = None
        self.expanded_nodes = 0

    def display_grid(self, grid, height, width):
        """Display the loaded game board."""
        # Display game board
        print("\n")
        print("\n")
        for row in range(height):
            for column in range(width):
                vehicle = grid[column][row]
                if vehicle:
                    print("%s " % vehicle.get_name(), end=" ")
                else:
                    print(". ", end=" ")

                if column == width - 1:
                    print("\n")

    def from_moves_to_grids(self, moves):
        """Convert moves to grids."""
        grids = [self.game_board.get_grid()]
        for move in moves:
            grid = deepcopy(grids[-1])
            vehicle = move[0]
            direction = move[1]
            old_locations = vehicle.get_occupied_locations()

            if direction == Direction.FORWARD:
                vehicle.move_forward()
            if direction == Direction.BACKWARD:
                vehicle.move_backward()

            new_locations = vehicle.get_occupied_locations()
            grid = self.update_vehicle(grid, vehicle, old_locations, new_locations)
            grids.append(grid)
        return grids

    def a_star_search(self, heuristic_name=None):
        """
        Search the node that has the lowest combined cost and heuristic first.
        """
        heuristic = None
        if heuristic_name == "null_heuristic":
            heuristic = null_heuristic
        elif heuristic_name == "blockingHeuristic":
            heuristic = blockingHeuristic
        elif heuristic_name == "distance_from_the_exit_Heuristic":
            heuristic = distance_from_the_exit_Heuristic
        elif heuristic_name == "distancePlusBlockingHeuristic":
            heuristic = distancePlusBlockingHeuristic

        prior_queue = util.PriorityQueue()
        visited = set()
        game_board = self.game_board
        nodes_info = Node(game_board.get_grid(), [], 0)
        # prior_queue.push(nodes_info, nodes_info.cost + null_heuristic(start_state, problem))
        prior_queue.push(nodes_info, nodes_info.cost + heuristic(game_board.get_grid(), game_board.get_height(), game_board.get_width()))

        while not prior_queue.isEmpty():
            node = prior_queue.pop()
            if self.is_solved(node.state):
                self.display_grid(node.state, self.game_board.get_height(), self.game_board.get_width())

                return node.path
            if hash(str(node.state)) in visited:
                continue

            # states.append([[[vehicle, direction]], new_grid])
            # vehicle == successor
            for [(vehicle, direction)], new_grid in self.get_states(node.state):
                # print("successor",vehicle)
                # print("direction",direction)
                # print("new_grid",new_grid)

                child_node = Node(new_grid, node.path + [(vehicle, direction)], node.cost + 1)
                prior_queue.push(child_node, child_node.cost + heuristic(child_node.state, game_board.get_height(), game_board.get_width()))
                # prior_queue.push(child_node, child_node.cost + null_heuristic(successor, problem))

            visited.add(hash(str(node.state)))

        return []

    def get_solution_BFS(self):
        """Run the breadth first search algorithm to find the solution."""
        grid = self.game_board.get_grid()
        visited = set()
        queue = [[[], grid]]

        while len(queue) > 0:
            for item in range(len(queue)):
                moves, grid = queue.pop(0)

                if self.is_solved(grid):
                    self.display_grid(grid, self.game_board.get_height(), self.game_board.get_width())
                    return moves

                for new_moves, new_grid in self.get_states(grid):
                    if hash(str(new_grid)) not in visited:
                        queue.append([moves + new_moves, new_grid])
                        visited.add(hash(str(new_grid)))

        self.display_grid(grid, self.game_board.get_height(), self.game_board.get_width())

        return None

    def get_states(self, grid):
        """Calculate different possible states"""
        states = []
        self.expanded_nodes += 1

        for row in range(self.game_board.get_height()):
            for column in range(self.game_board.get_width()):
                vehicle = grid[column][row]
                if vehicle and vehicle.type != "broken_down":
                    for direction in Direction:
                        if self.is_movable(vehicle, direction, grid):
                            new_grid = deepcopy(grid)

                            new_vehicle = new_grid[column][row]

                            if direction == Direction.BACKWARD:
                                new_vehicle.move_backward()

                            if direction == Direction.FORWARD:
                                new_vehicle.move_forward()

                            old_locations = vehicle.get_occupied_locations()
                            new_locations = new_vehicle.get_occupied_locations()
                            new_grid = self.update_vehicle(new_grid, new_vehicle, old_locations, new_locations)
                            states.append([[[vehicle, direction]], new_grid])
        return states

    @staticmethod
    def update_vehicle(grid, vehicle, old_locations, new_locations):
        """Update grid with the vehicles' new location."""
        for location in old_locations:
            x = location["x"]
            y = location["y"]
            grid[x][y] = 0

        for location in new_locations:
            x = location["x"]
            y = location["y"]
            grid[x][y] = vehicle

        return grid

    def is_movable(self, vehicle, direction, grid):
        """Check if vehicle object is movable to the next empty space."""
        if vehicle.get_orientation() == Orientation.HORIZONTAL and direction == Direction.FORWARD:
            location = vehicle.get_end_location()
            x = location["x"] + 1
            y = location["y"]

            if x < self.game_board.get_width():
                board_vehicle = grid[x][y]
                if board_vehicle:
                    return False
            else:
                return False

        if vehicle.get_orientation() == Orientation.HORIZONTAL and direction == Direction.BACKWARD:
            location = vehicle.get_start_location()
            x = location["x"] - 1
            y = location["y"]

            if x > -1:
                board_vehicle = grid[x][y]
                if board_vehicle:
                    return False
            else:
                return False

        if vehicle.get_orientation() == Orientation.VERTICAL and direction == Direction.FORWARD:
            location = vehicle.get_end_location()
            x = location["x"]
            y = location["y"] + 1

            if y < self.game_board.get_height():
                board_vehicle = grid[x][y]
                if board_vehicle:
                    return False
            else:
                return False

        if vehicle.get_orientation() == Orientation.VERTICAL and direction == Direction.BACKWARD:
            location = vehicle.get_start_location()
            x = location["x"]
            y = location["y"] - 1

            if y > -1:
                board_vehicle = grid[x][y]
                if board_vehicle:
                    return False
            else:
                return False

        return True

    def is_solved(self, grid):
        """Check if game board is solved."""
        for row in range(self.game_board.get_height()):
            for column in range(self.game_board.get_width()):
                vehicle = grid[column][row]

                if vehicle and vehicle.is_main_vehicle() and column == self.game_board.get_width() - 1:
                    return True
        return False


def distancePlusBlockingHeuristic(grid, height, width):
    num_vehicles = 0
    main_vehicle = None
    for row in range(height):
        for column in range(width):
            vehicle = grid[column][row]

            if vehicle and vehicle.is_main_vehicle():
                main_vehicle = (row, column)

    for column in range(main_vehicle[1], width):
        vehicle = grid[column][main_vehicle[0]]
        if vehicle and not vehicle.is_main_vehicle():
            num_vehicles += 1

    # print("num_vehicles" , num_vehicles)
    return num_vehicles + (width - main_vehicle[1] - 1)


# How many cars are blocking the red car from exiting
def distance_from_the_exit_Heuristic(grid, height, width):
    main_vehicle = None
    for row in range(height):
        for column in range(width):
            vehicle = grid[column][row]

            if vehicle and vehicle.is_main_vehicle():
                main_vehicle = (row, column)

    return width - main_vehicle[1] - 1


# How many cars are blocking the red car from exiting
def blockingHeuristic(grid, height, width):
    num_vehicles = 0
    main_vehicle = None
    for row in range(height):
        for column in range(width):
            vehicle = grid[column][row]

            if vehicle and vehicle.is_main_vehicle():
                main_vehicle = (row, column)

    for column in range(main_vehicle[1], width):
        vehicle = grid[column][main_vehicle[0]]
        if vehicle and not vehicle.is_main_vehicle():
            num_vehicles += 1

    # print("num_vehicles" , num_vehicles)
    return num_vehicles


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
