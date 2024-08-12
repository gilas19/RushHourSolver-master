import time
from controllers.board_loader import BoardLoader
from controllers.board_solver import BoardSolver
from display import ConsoleView, GUIView
from optparse import OptionParser


class RushHourGame:
    """Class representing the Rush Hour game solver."""

    def __init__(self, options):
        """Initialize the Rush Hour game solver with provided options."""
        self.loader = BoardLoader()
        self.display = GUIView() if options.display == "gui" else ConsoleView()
        self.algorithm = options.algorithm
        self.heuristic = options.heuristic

    def run(self, board_file):
        """Execute the game solver and display the results."""
        # Load the game board from the specified file
        board = self.loader.load(f"./boards/{board_file}.txt")

        # Solve the game board using the selected algorithm
        start_time = time.perf_counter()
        solver = BoardSolver(board)
        solution = self.solve_board(solver)
        end_time = time.perf_counter()
        time_delta = end_time - start_time

        # Display the solution and statistics
        self.display_results(solver, solution, time_delta)

    def solve_board(self, solver):
        """Solve the board using the selected algorithm."""
        match self.algorithm:
            case "bfs":
                return solver.get_solution_BFS()
            case "dfs":
                return solver.dfs_search()
            case "a_star":
                return solver.a_star_search(self.heuristic)
            case _:
                raise ValueError(f"Unknown algorithm: {self.algorithm}")

    def display_results(self, solver, solution, time_delta):
        """Display the solution and statistics."""
        if solution:
            grids = solver.from_moves_to_grids(solution)
            possible_moves = [solver.get_states(grid) for grid in grids]
            self.display.show_solution(solver.game_board, grids, possible_moves)
            self.display.show_statistics(time_delta, solver.expanded_nodes, len(solution))
        else:
            print("No solution found!")
            self.display.show_statistics(time_delta, solver.expanded_nodes)


def main():
    """Main function to parse command-line options and start the game."""
    usage_str = """
    USAGE:      python game.py <options>
    EXAMPLES:   python game.py
                OR python game.py --board beginner --display gui --algorithm bfs --heuristic null_heuristic
                    - Starts the game with the beginner board, GUI display, BFS algorithm, and null heuristic.
    """
    parser = OptionParser(usage=usage_str)
    parser.add_option("-b", "--board", dest="board_file", default="advance", help="Board file name.")
    parser.add_option("-d", "--display", dest="display", default="gui", help="Display type (gui or console).")
    parser.add_option("-f", "--algorithm", dest="algorithm", default="a_star", help="Search algorithm to use.")
    parser.add_option("--heuristic", dest="heuristic", default="blockingHeuristic", help="Heuristic function for A*.")

    (options, args) = parser.parse_args()

    try:
        rush_hour_solver = RushHourGame(options)
        rush_hour_solver.run(options.board_file)
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
