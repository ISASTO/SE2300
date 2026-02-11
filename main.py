# main.py
import sys
import pygame

from maze import Maze
from generator import MazeGenerator
from player import Player
from renderer import Renderer
from ui import UIControls


# Window size
WINDOW_W = 900
WINDOW_H = 960

# Top UI bar height
UI_BAR_H = 70

# Frame rate cap
FPS = 60


# Simple game states
STATE_WAITING = "WAITING"
STATE_PLAYING = "PLAYING"
STATE_WON = "WON"


def build_solution_path(maze, start_cell, finish_cell):
    """
    Build a solution path as a list of cells from start to finish.
    Uses Breadth-First Search.
    """
    from collections import deque

    q = deque()
    q.append(start_cell)

    came_from = {start_cell: None}

    while q:
        cur = q.popleft()
        if cur == finish_cell:
            break

        for nxt in maze.get_neighbors(cur):
            if nxt not in came_from:
                came_from[nxt] = cur
                q.append(nxt)

    if finish_cell not in came_from:
        return []

    # Reconstruct path backwards
    path = []
    cur = finish_cell
    while cur is not None:
        path.append(cur)
        cur = came_from[cur]
    path.reverse()
    return path


def main():
    pygame.init()
    pygame.display.set_caption("Maze Game")

    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    clock = pygame.time.Clock()

    generator = MazeGenerator()
    renderer = Renderer(window_w=WINDOW_W, window_h=WINDOW_H, ui_bar_h=UI_BAR_H)
    ui = UIControls(window_w=WINDOW_W, ui_bar_h=UI_BAR_H)
    player = Player()

    maze = None
    game_state = STATE_WAITING

    # Easter egg solve path
    solution_path = []
    show_solution = False

    # Typed buffer for "solve"
    typed_buffer = ""

    # Create a default maze so the window isn't blank
    default_size = 10
    maze = generator.generate(default_size)
    player.reset(maze.start_cell)
    solution_path = build_solution_path(maze, maze.start_cell, maze.finish_cell)
    game_state = STATE_PLAYING
    ui.set_status("Maze generated. Use arrow keys to move.")

    running = True
    while running:
        dt_ms = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            # Mouse clicks for UI
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ui.handle_mouse_click(event.pos)

            if event.type == pygame.KEYDOWN:
                # Feed typing to the UI first (for size input)
                ui.handle_key_down(event.key, event.unicode)

                # Track typed letters for "solve"
                if event.unicode and event.unicode.isprintable():
                    typed_buffer += event.unicode.lower()
                    typed_buffer = typed_buffer[-10:]  # keep it short

                # If user typed "solve", toggle solution overlay
                if "solve" in typed_buffer:
                    show_solution = not show_solution
                    typed_buffer = ""
                    if show_solution:
                        ui.set_status("Solution overlay ON.")
                    else:
                        ui.set_status("Solution overlay OFF.")

                # Arrow keys move the player, but only if game is active
                if maze is not None and game_state in (STATE_PLAYING,):
                    direction = None
                    if event.key == pygame.K_UP:
                        direction = "N"
                    elif event.key == pygame.K_RIGHT:
                        direction = "E"
                    elif event.key == pygame.K_DOWN:
                        direction = "S"
                    elif event.key == pygame.K_LEFT:
                        direction = "W"

                    if direction is not None:
                        moved = player.try_move(direction, maze)
                        if moved:
                            # Win check
                            if player.current_cell == maze.finish_cell:
                                game_state = STATE_WON
                                ui.set_status("You won! Click Generate for a new maze.")
                        else:
                            # No move is fine, just don't spam status
                            pass

        # If the UI says "generate was clicked", try to generate a new maze
        if ui.consume_generate_clicked():
            size, err = ui.get_requested_size()
            if err is not None:
                ui.set_error(err)
            else:
                maze = generator.generate(size)
                player.reset(maze.start_cell)
                solution_path = build_solution_path(maze, maze.start_cell, maze.finish_cell)
                show_solution = False
                game_state = STATE_PLAYING
                ui.set_status(f"Generated {size}x{size} maze. Use arrow keys to move.")

        # Draw everything
        renderer.render(
            screen=screen,
            maze=maze,
            player=player,
            ui=ui,
            game_state=game_state,
            solution_path=solution_path if show_solution else []
        )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()