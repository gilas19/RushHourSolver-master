import time
from controllers.board_loader import BoardLoader
from controllers.board_solver import BoardSolver
from display import ConsoleView, GUIView
from optparse import OptionParser


class RushHourGame(object):
    """Rush Hour Game class."""

    def __init__(self, options):
        """Initialize the Rush Hour Solver."""
        self.loader = BoardLoader()
        self.display = GUIView() if options.display == "gui" else ConsoleView()
        self.algorithm = options.algorithm
        self.heuristic = options.heuristic

    def run(self, board_file):
        """Run Application."""
        # Load game board from file
        board = self.loader.load(f"./boards/{board_file}.txt")

        # Find the solution to the game board
        start_time = time.perf_counter()
        solver = BoardSolver(board)
        match self.algorithm:
            case "bfs":
                solution = solver.get_solution_BFS()
            case "dfs":
                solution = solver.dfs_search()
            case "a_star":
                solution = solver.a_star_search(self.heuristic)
        end_time = time.perf_counter()
        time_delta = end_time - start_time

        # Display the solution
        if solution:
            grids = solver.from_moves_to_grids(solution)
            possible_moves = [solver.get_states(grid) for grid in grids]
            self.display.show_solution(board, grids, possible_moves)
            self.display.show_statistics(time_delta, solver.expanded_nodes, len(solution))
        else:
            print("No solution found!")
            self.display.show_statistics(time_delta, solver.expanded_nodes)


def main():
    # distance_from_the_exit_Heuristic
    # blockingHeuristic
    # null_heuristic
    # distancePlusBlockingHeuristic

    usage_str = """
    USAGE:      python game.py <options>
    EXAMPLES:   python game.py
                OR python game.py --board beginner --display gui --algorithm bfs --heuristic null_heuristic
                    - starts a game with beginner board, GUI display, BFS algorithm and null heuristic
                
                
                
    """
    parser = OptionParser(usage_str)
    parser.add_option("-b", "--board", dest="board_file", default="beginner", help="board file name")
    parser.add_option("-d", "--display", dest="display", default="gui", help="display type (gui or console)")
    parser.add_option("-f", "--algorithm", dest="algorithm", default="a_star", help="search algorithm")
    parser.add_option("--heuristic", dest="heuristic", default="blockingHeuristic", help="heuristic function")
    (options, args) = parser.parse_args()

    rush_hour_solver = RushHourGame(options)
    rush_hour_solver.run(options.board_file)


if __name__ == "__main__":
    main()
