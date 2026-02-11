# generator.py
import random
from maze import Maze


class MazeGenerator:
    """
    Generates a perfect maze using randomized DFS backtracking.
    Perfect maze = exactly one path between any two cells.
    """
    def __init__(self, random_seed=None):
        self.random_seed = random_seed

    def generate(self, size):
        if self.random_seed is not None:
            random.seed(self.random_seed)

        maze = Maze(size)

        # Stack for DFS backtracking
        stack = []

        start = maze.start_cell
        start.visited = True
        current = start

        total = size * size
        visited_count = 1

        while visited_count < total:
            neighbors = self._get_unvisited_neighbors(maze, current)

            if neighbors:
                # Pick a random unvisited neighbor
                nxt = random.choice(neighbors)

                # Carve path
                maze.remove_wall_between(current, nxt)

                # Push current for backtracking later
                stack.append(current)

                # Move to neighbor
                current = nxt
                current.visited = True
                visited_count += 1
            else:
                # Dead end, backtrack
                if stack:
                    current = stack.pop()
                else:
                    # Should not happen in a normal DFS maze, good to have anyway
                    break

        # Clear visited flags so they don't confuse other logic
        for row in maze.cells:
            for cell in row:
                cell.visited = False

        return maze

    def _get_unvisited_neighbors(self, maze, cell):
        out = []
        for d in ("N", "E", "S", "W"):
            nxt = maze.get_adjacent(cell, d)
            if nxt is not None and not nxt.visited:
                out.append(nxt)
        return out
