# player.py
class Player:
    """
    Tracks current position and a trail that disappears when backtracking.
    """
    def __init__(self):
        self.current_cell = None
        self.trail = []  # list of cells, in order

    def reset(self, start_cell):
        self.current_cell = start_cell
        self.trail = [start_cell]

    def try_move(self, direction, maze):
        """
        Attempt to move in a direction.
        - If blocked by a wall or edge: do nothing, return False
        - If move succeeds:
            - If new cell is the previous trail cell, pop (backtrack)
            - Otherwise append (forward move)
        """
        if self.current_cell is None:
            return False

        if not maze.can_move(self.current_cell, direction):
            return False

        nxt = maze.get_adjacent(self.current_cell, direction)
        if nxt is None:
            return False

        # Backtracking behavior
        if len(self.trail) >= 2 and nxt == self.trail[-2]:
            # Move back one step, remove last cell from trail
            self.trail.pop()
            self.current_cell = nxt
            return True

        # Forward move
        self.current_cell = nxt
        self.trail.append(nxt)
        return True
