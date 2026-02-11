# maze.py
class Cell:
    """
    One cell in the maze grid.
    Walls start as True (present). Maze generation removes walls to carve paths.
    """
    __slots__ = ("row", "col", "wall_n", "wall_e", "wall_s", "wall_w", "visited")

    def __init__(self, row, col):
        self.row = row
        self.col = col

        # Walls exist at the start
        self.wall_n = True
        self.wall_e = True
        self.wall_s = True
        self.wall_w = True

        # Used by generator
        self.visited = False

    def __repr__(self):
        return f"Cell({self.row},{self.col})"


class Maze:
    """
    Holds a grid of cells plus helper functions for movement and neighbor lookup.
    """
    def __init__(self, size):
        self.size = size

        # 2D grid: cells[row][col]
        self.cells = [[Cell(r, c) for c in range(size)] for r in range(size)]

        self.start_cell = self.cells[0][0]
        self.finish_cell = self.cells[size - 1][size - 1]

    def get_cell(self, row, col):
        return self.cells[row][col]

    def in_bounds(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def get_adjacent(self, cell, direction):
        """
        Return the adjacent cell in a direction, or None if out of bounds.
        Direction is 'N', 'E', 'S', or 'W'
        """
        dr, dc = 0, 0
        if direction == "N":
            dr = -1
        elif direction == "E":
            dc = 1
        elif direction == "S":
            dr = 1
        elif direction == "W":
            dc = -1

        nr = cell.row + dr
        nc = cell.col + dc
        if not self.in_bounds(nr, nc):
            return None
        return self.cells[nr][nc]

    def has_wall(self, cell, direction):
        if direction == "N":
            return cell.wall_n
        if direction == "E":
            return cell.wall_e
        if direction == "S":
            return cell.wall_s
        if direction == "W":
            return cell.wall_w
        return True

    def remove_wall_between(self, a, b):
        """
        Remove walls between two adjacent cells (both directions)
        """
        dr = b.row - a.row
        dc = b.col - a.col

        if dr == -1 and dc == 0:
            # b is north of a
            a.wall_n = False
            b.wall_s = False
        elif dr == 1 and dc == 0:
            # b is south of a
            a.wall_s = False
            b.wall_n = False
        elif dr == 0 and dc == 1:
            # b is east of a
            a.wall_e = False
            b.wall_w = False
        elif dr == 0 and dc == -1:
            # b is west of a
            a.wall_w = False
            b.wall_e = False

    def can_move(self, from_cell, direction):
        """
        Move is allowed if there's no wall in that direction and the target exists.
        """
        if self.has_wall(from_cell, direction):
            return False
        nxt = self.get_adjacent(from_cell, direction)
        return nxt is not None

    def get_neighbors(self, cell):
        """
        Return all reachable neighbors (no walls).
        Useful for solution finding
        """
        out = []
        for d in ("N", "E", "S", "W"):
            if not self.has_wall(cell, d):
                nxt = self.get_adjacent(cell, d)
                if nxt is not None:
                    out.append(nxt)
        return out
