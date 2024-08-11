import matplotlib.pyplot as plt
import matplotlib.patches as patches


class GameBoard:
    """Represents the game board for the Rush Hour game."""

    def __init__(self, height, width):
        """Initialize the game board with specified dimensions."""
        self.height = height
        self.width = width
        self.grid = self.generate_grid()

    def generate_grid(self):
        """Generate an empty grid based on the board dimensions."""
        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def get_grid(self):
        """Return the current state of the grid."""
        return self.grid

    def add_vehicle(self, vehicle, locations):
        """Place a vehicle on the board at specified locations.

        Args:
            vehicle: The vehicle object to be placed on the board.
            locations (list of dicts): A list of locations where the vehicle occupies, each location
                                       is represented as a dictionary with 'x' and 'y' keys.
        """
        for location in locations:
            x, y = location["x"], location["y"]
            if self.is_within_bounds(x, y):
                self.grid[x][y] = vehicle
            else:
                raise ValueError(f"Location ({x}, {y}) is out of bounds for the board.")

    def is_within_bounds(self, x, y):
        """Check if the given coordinates are within the bounds of the board."""
        return 0 <= x < self.height and 0 <= y < self.width

    def get_height(self):
        """Return the height of the game board."""
        return self.height

    def get_width(self):
        """Return the width of the game board."""
        return self.width
