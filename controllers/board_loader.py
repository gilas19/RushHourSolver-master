import re
from models.game_board import GameBoard
from models.vehicle import Vehicle


class BoardLoader(object):

    def __init__(self):
        self.filename = None
        self.game_board = None

    def load(self, filename):
        """Load the game board file."""
        self.filename = filename
        content = self.read()
        self.validate(content)
        self.parse_to_objects(content)
        return self.game_board

    def read(self):
        """Read the game board file."""
        try:
            with open(self.filename, "r") as file:
                return file.read().splitlines()
        except FileNotFoundError:
            print("File with board data not found! Please enter correct file location.")

    def parse_to_objects(self, content):
        """Parse the game board file into the corresponding models."""
        vehicles = {}
        vehicle_type = None

        for row_index, line in enumerate(content):
            for column_index, letter in enumerate(line):
                if letter == "X":
                    vehicle_type = "main"
                elif letter.isupper():
                    vehicle_type = "vehicle"
                elif letter.islower():
                    vehicle_type = "broken_down"
                else:
                    continue

                if letter not in vehicles:
                    vehicle = Vehicle(name=letter, type=vehicle_type)
                    vehicle.set_start_location(column_index, row_index)
                    vehicles[letter] = vehicle
                else:
                    vehicle = vehicles[letter]
                    vehicle.set_end_location(column_index, row_index)

        board_width = len(content[0])
        board_height = len(content)
        self.game_board = GameBoard(board_height, board_width)

        for _, vehicle in sorted(vehicles.items()):
            locations = vehicle.get_occupied_locations()
            self.game_board.add_vehicle(vehicle, locations)

    def get_game_board(self):
        """Return the loaded game board."""
        return self.game_board

    @staticmethod
    def validate(content):
        """Validate the content of the game board file."""
        try:
            if len(content) == 0:
                raise ValueError("The file is empty! Please select a file with a correct data format.")

            line_length = len(content[0])
            red_car_size = 0
            for line in content:
                if line_length != len(line):
                    raise ValueError("The data format is not correct! All the text lines need to be the same length.")

                if re.sub(r"[A-Za-z.]+", "", line):
                    raise ValueError('The data format is not correct! Only letters and "." are allowed.')

                if "X" in line:
                    red_car_size += 1

            if red_car_size == 0:
                raise ValueError("The data format is not correct! The red car is not set.")

        except ValueError as expression:
            print(expression)
