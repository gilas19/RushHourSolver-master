import re
from models.game_board import GameBoard
from models.vehicle import Vehicle


class BoardLoader:
    """Class responsible for loading and parsing a game board file."""

    def __init__(self):
        self.filename = None
        self.game_board = None

    def load(self, filename):
        """Load the game board from the specified file."""
        self.filename = filename
        content = self.read()
        self.validate(content)
        self.parse_to_objects(content)
        return self.game_board

    def read(self):
        """Read the content of the game board file."""
        try:
            with open(self.filename, "r") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self.filename}' not found! Please provide the correct file location.")

    def parse_to_objects(self, content):
        """Parse the game board content into vehicle and board objects."""
        vehicles = {}

        for row_index, line in enumerate(content):
            for column_index, letter in enumerate(line):
                vehicle_type = self.determine_vehicle_type(letter)
                if vehicle_type:
                    if letter not in vehicles:
                        vehicle = Vehicle(name=letter, type=vehicle_type)
                        vehicle.set_start_location(column_index, row_index)
                        vehicles[letter] = vehicle
                    else:
                        vehicle = vehicles[letter]
                        vehicle.set_end_location(column_index, row_index)

        self.initialize_game_board(content, vehicles)

    def determine_vehicle_type(self, letter):
        """Determine the type of vehicle based on the letter."""
        if letter == "X":
            return "main"
        elif letter.isupper():
            return "vehicle"
        elif letter.islower():
            return "broken_down"
        return None

    def initialize_game_board(self, content, vehicles):
        """Initialize the game board with vehicles placed on it."""
        board_width = len(content[0])
        board_height = len(content)
        self.game_board = GameBoard(board_height, board_width)

        for vehicle in sorted(vehicles.values(), key=lambda v: v.name):
            locations = vehicle.get_occupied_locations()
            self.game_board.add_vehicle(vehicle, locations)

    def get_game_board(self):
        """Return the loaded game board."""
        return self.game_board

    @staticmethod
    def validate(content):
        """Validate the content of the game board file."""
        if not content:
            raise ValueError("The file is empty! Please select a file with the correct data format.")

        line_length = len(content[0])
        red_car_size = 0

        for line in content:
            if len(line) != line_length:
                raise ValueError("The data format is incorrect! All text lines must be the same length.")
            if re.sub(r"[A-Za-z.]+", "", line):
                raise ValueError("The data format is incorrect! Only letters and '.' are allowed.")
            if "X" in line:
                red_car_size += 1

        if red_car_size == 0:
            raise ValueError("The data format is incorrect! The red car is not set.")
