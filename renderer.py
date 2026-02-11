# renderer.py
import pygame


class Renderer:
    """
    Draws:
    - UI bar
    - Maze walls
    - Trail (red)
    - Player (blue)
    - Finish cell (green outline)
    - Optional solution overlay (yellow)
    """
    def __init__(self, window_w, window_h, ui_bar_h):
        self.window_w = window_w
        self.window_h = window_h
        self.ui_bar_h = ui_bar_h

        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        self.big_font = pygame.font.SysFont(None, 42)

    def render(self, screen, maze, player, ui, game_state, solution_path):
        screen.fill((18, 18, 18))

        # UI bar background
        pygame.draw.rect(screen, (30, 30, 30), (0, 0, self.window_w, self.ui_bar_h))

        # Draw UI elements
        self._draw_ui(screen, ui)

        if maze is None:
            return

        # Compute cell size to fit below UI bar
        grid_w = self.window_w
        grid_h = self.window_h - self.ui_bar_h

        cell_size = min(grid_w // maze.size, grid_h // maze.size)
        if cell_size < 2:
            cell_size = 2

        offset_x = (grid_w - cell_size * maze.size) // 2
        offset_y = self.ui_bar_h + (grid_h - cell_size * maze.size) // 2

        # Trail fill (light red)
        if player.current_cell is not None:
            for c in player.trail:
                x = offset_x + c.col * cell_size
                y = offset_y + c.row * cell_size
                pygame.draw.rect(screen, (120, 40, 40), (x, y, cell_size, cell_size))

        # Optional solution overlay (highlights with yellow squares)
        if solution_path:
            for c in solution_path:
                x = offset_x + c.col * cell_size
                y = offset_y + c.row * cell_size
                pygame.draw.rect(screen, (180, 180, 60), (x + 2, y + 2, cell_size - 4, cell_size - 4), 2)

        # Finish cell outline
        f = maze.finish_cell
        fx = offset_x + f.col * cell_size
        fy = offset_y + f.row * cell_size
        pygame.draw.rect(screen, (60, 180, 80), (fx, fy, cell_size, cell_size), 3)

        # Maze walls
        wall_color = (230, 230, 230)
        for r in range(maze.size):
            for c in range(maze.size):
                cell = maze.cells[r][c]
                x = offset_x + c * cell_size
                y = offset_y + r * cell_size

                if cell.wall_n:
                    pygame.draw.line(screen, wall_color, (x, y), (x + cell_size, y), 2)
                if cell.wall_e:
                    pygame.draw.line(screen, wall_color, (x + cell_size, y), (x + cell_size, y + cell_size), 2)
                if cell.wall_s:
                    pygame.draw.line(screen, wall_color, (x, y + cell_size), (x + cell_size, y + cell_size), 2)
                if cell.wall_w:
                    pygame.draw.line(screen, wall_color, (x, y), (x, y + cell_size), 2)

        # Player dot (blue)
        if player.current_cell is not None:
            pc = player.current_cell
            cx = offset_x + pc.col * cell_size + cell_size // 2
            cy = offset_y + pc.row * cell_size + cell_size // 2
            radius = max(3, cell_size // 3)
            pygame.draw.circle(screen, (60, 120, 255), (cx, cy), radius)

        # Win overlay
        if game_state == "WON":
            self._draw_win(screen)

    def _draw_ui(self, screen, ui):
        # Input box border changes when active
        input_border = (255, 255, 255) if ui.active_input else (180, 180, 180)

        pygame.draw.rect(screen, (50, 50, 50), ui.input_rect, border_radius=6)
        pygame.draw.rect(screen, input_border, ui.input_rect, 2, border_radius=6)

        # Put the label inside the visible UI area
        label = self.font.render("Size:", True, (220, 220, 220))
        screen.blit(label, (ui.input_rect.x, ui.input_rect.y - 16))

        # Draw input text
        txt = ui.size_text if ui.size_text != "" else ""
        t_surf = self.font.render(txt, True, (240, 240, 240))
        text_x = ui.input_rect.x + 10
        text_y = ui.input_rect.y + 8
        screen.blit(t_surf, (text_x, text_y))

        # Blinking cursor when active
        if ui.active_input:
            ticks = pygame.time.get_ticks()
            if (ticks // 500) % 2 == 0:
                cursor_x = text_x + t_surf.get_width() + 2
                cursor_y0 = ui.input_rect.y + 8
                cursor_y1 = ui.input_rect.y + ui.input_rect.h - 8
                pygame.draw.line(screen, (240, 240, 240), (cursor_x, cursor_y0), (cursor_x, cursor_y1), 2)

        # Generate button
        pygame.draw.rect(screen, (70, 70, 70), ui.button_rect, border_radius=6)
        pygame.draw.rect(screen, (220, 220, 220), ui.button_rect, 2, border_radius=6)
        b_surf = self.font.render("Generate", True, (240, 240, 240))
        screen.blit(b_surf, (ui.button_rect.x + 18, ui.button_rect.y + 8))

        # Status message
        color = (255, 120, 120) if ui.is_error else (220, 220, 220)
        msg = self.font.render(ui.status_message, True, color)
        screen.blit(msg, (310, 26))

    def _draw_win(self, screen):
        overlay = pygame.Surface((self.window_w, self.window_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        text = self.big_font.render("YOU WIN", True, (255, 255, 255))
        rect = text.get_rect(center=(self.window_w // 2, self.window_h // 2))
        screen.blit(text, rect)