# ui.py
import pygame


class UIControls:
    """
    Very simple UI:
    - size input box (type digits)
    - generate button
    - status line
    """
    def __init__(self, window_w, ui_bar_h):
        self.window_w = window_w
        self.ui_bar_h = ui_bar_h

        # Input state
        self.size_text = "10"
        self.active_input = False

        # Status messages
        self.status_message = "Ready."
        self.is_error = False

        # Button flags
        self._generate_clicked = False

        # UI layout
        self.input_rect = pygame.Rect(20, 18, 120, 34)
        self.button_rect = pygame.Rect(160, 18, 120, 34)

    def set_status(self, text):
        self.status_message = text
        self.is_error = False

    def set_error(self, text):
        self.status_message = text
        self.is_error = True

    def handle_mouse_click(self, pos):
        # Clicking input box toggles typing focus w/ blinking cursor
        if self.input_rect.collidepoint(pos):
            self.active_input = True
        else:
            self.active_input = False

        # Clicking Generate requests generation
        if self.button_rect.collidepoint(pos):
            self._generate_clicked = True

    def handle_key_down(self, key, unicode_char):
        """
        If input box is active, accept digits and backspace.
        """
        if not self.active_input:
            return

        if key == pygame.K_BACKSPACE:
            self.size_text = self.size_text[:-1]
            return

        # Only allow digits in the size box
        if unicode_char.isdigit():
            # Keep it 3 characters or less
            if len(self.size_text) < 3:
                self.size_text += unicode_char

    def consume_generate_clicked(self):
        """
        One-shot flag so main can react once per click.
        """
        if self._generate_clicked:
            self._generate_clicked = False
            return True
        return False

    def get_requested_size(self):
        """
        Returns (size_int, err_string_or_None).
        """
        text = self.size_text.strip()
        if text == "":
            return None, "Please enter an integer in the range of 3 to 100."

        try:
            size = int(text)
        except ValueError:
            return None, "Please enter an integer in the range of 3 to 100."

        if size < 3 or size > 100:
            return None, "Please enter an integer in the range of 3 to 100."

        return size, None