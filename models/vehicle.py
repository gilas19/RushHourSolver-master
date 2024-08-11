from util import Orientation


class Vehicle(object):
    """Vehicle class."""

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
        self.name = name
        self.start = {}
        self.end = {}
        self.type = type  # main, vehicle, broken_down
        self.occupied_locations = []
        self.color = self.VEHICLE_COLORS.get(name, "black")

    def set_start_location(self, x, y):
        """Set start location of the object."""
        self.start["x"] = x
        self.start["y"] = y

    def get_start_location(self):
        """Get start location of the object."""
        return self.start

    def set_end_location(self, x, y):
        """Set end location of the object."""
        self.end["x"] = x
        self.end["y"] = y

    def get_end_location(self):
        """Get end location of the object."""
        return self.end

    def get_occupied_locations(self):
        """Get the locations that are being occupied by the objects."""
        occupied_locations = []

        if self.get_orientation() == Orientation.HORIZONTAL:
            delta = self.end["x"] - self.start["x"]
            for index in range(0, delta + 1):
                location = {"x": self.start["x"] + index, "y": self.start["y"]}
                occupied_locations.append(location)

        if self.get_orientation() == Orientation.VERTICAL:
            delta = self.end["y"] - self.start["y"]
            for index in range(0, delta + 1):
                location = {"x": self.start["x"], "y": self.start["y"] + index}
                occupied_locations.append(location)

        self.occupied_locations = occupied_locations
        return occupied_locations

    def set_name(self, name):
        """Set name of the object."""
        self.name = name

    def get_name(self):
        """Get name of the object."""
        return self.name

    def is_main_vehicle(self):
        """Check if the object is the main vehicle (Red Car)"""
        return self.type == "main"

    def get_orientation(self):
        """Get the orientation of the object."""
        if self.start["x"] == self.end["x"]:
            return Orientation.VERTICAL

        if self.start["y"] == self.end["y"]:
            return Orientation.HORIZONTAL

    def move_forward(self):
        """Move the object a space forward."""
        if self.get_orientation() == Orientation.HORIZONTAL:
            self.start["x"] += 1
            self.end["x"] += 1

        if self.get_orientation() == Orientation.VERTICAL:
            self.start["y"] += 1
            self.end["y"] += 1

    def move_backward(self):
        """Move the object a space backward."""
        if self.get_orientation() == Orientation.HORIZONTAL:
            self.start["x"] -= 1
            self.end["x"] -= 1

        if self.get_orientation() == Orientation.VERTICAL:
            self.start["y"] -= 1
            self.end["y"] -= 1

    def __repr__(self):
        # return "%s - %s - %s" % (self.name, self.start, self.end)
        return self.name
