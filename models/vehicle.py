from util import Orientation


class Vehicle:
    """Represents a vehicle on the Rush Hour game board."""

    VEHICLE_COLORS = {
        "X": "red",
        "A": "yellowgreen",
        "B": "gold",
        "C": "mediumpurple",
        "D": "pink",
        "E": "purple",
        "F": "turquoise",
        "G": "gray",
        "H": "tan",
        "I": "yellow",
        "J": "silver",
        "K": "white",
        "O": "orange",
        "P": "pink",
        "Q": "blue",
        "R": "green",
    }

    def __init__(self, name, type):
        """Initialize a vehicle with a name and type."""
        self.name = name
        self.type = type  # main, vehicle, broken_down
        self.start = {"x": None, "y": None}
        self.end = {"x": None, "y": None}
        self.color = self.VEHICLE_COLORS.get(name, "black")
        self.occupied_locations = []

    def set_start_location(self, x, y):
        """Set the start location of the vehicle."""
        self.start = {"x": x, "y": y}

    def get_start_location(self):
        """Return the start location of the vehicle."""
        return self.start

    def set_end_location(self, x, y):
        """Set the end location of the vehicle."""
        self.end = {"x": x, "y": y}

    def get_end_location(self):
        """Return the end location of the vehicle."""
        return self.end

    def get_occupied_locations(self):
        """Calculate and return the list of locations occupied by the vehicle."""
        self.occupied_locations = []

        if self.get_orientation() == Orientation.HORIZONTAL:
            self.occupied_locations = [{"x": self.start["x"] + i, "y": self.start["y"]} for i in range(self.end["x"] - self.start["x"] + 1)]
        elif self.get_orientation() == Orientation.VERTICAL:
            self.occupied_locations = [{"x": self.start["x"], "y": self.start["y"] + i} for i in range(self.end["y"] - self.start["y"] + 1)]

        return self.occupied_locations

    def get_name(self):
        """Return the name of the vehicle."""
        return self.name

    def is_main_vehicle(self):
        """Check if the vehicle is the main (red car) vehicle."""
        return self.type == "main"

    def get_orientation(self):
        """Determine and return the orientation of the vehicle."""
        if self.start["x"] == self.end["x"]:
            return Orientation.VERTICAL
        elif self.start["y"] == self.end["y"]:
            return Orientation.HORIZONTAL
        else:
            raise ValueError("Invalid vehicle position: Start and end points do not align horizontally or vertically.")

    def move_forward(self):
        """Move the vehicle one step forward."""
        if self.get_orientation() == Orientation.HORIZONTAL:
            self.start["x"] += 1
            self.end["x"] += 1
        elif self.get_orientation() == Orientation.VERTICAL:
            self.start["y"] += 1
            self.end["y"] += 1

    def move_backward(self):
        """Move the vehicle one step backward."""
        if self.get_orientation() == Orientation.HORIZONTAL:
            self.start["x"] -= 1
            self.end["x"] -= 1
        elif self.get_orientation() == Orientation.VERTICAL:
            self.start["y"] -= 1
            self.end["y"] -= 1

    def __repr__(self):
        """Return a string representation of the vehicle."""
        # return f"{self.name} - {self.start} to {self.end}"
        return self.name
