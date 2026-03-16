"""Provides window management and view navigation state for the LogicBox application."""

import arcade
from modules.data import data
from typing import List


class Window:
    """Manages the main application window and provides a stack-based navigation system."""

    def __init__(self) -> None:
        """Initializes the window instance with configuration settings and navigation state."""
        self.width: int = data.WINDOW_WIDTH
        self.height: int = data.WINDOW_HEIGHT
        self.title: str = "LogicBox"

        self.window: arcade.Window = arcade.Window(
            self.width,
            self.height,
            self.title,
            fullscreen=data.WINDOW_FULLSCREEN,
            # Set update and draw rates to approximately 60 FPS
            update_rate=1 / 60,
            draw_rate=1 / 60,
        )

        self.view_history: List[arcade.View] = []

    def back(self) -> None:
        """Navigates to the previous view in the history stack."""
        self.view_history.pop()
        view: arcade.View = self.view_history[-1]
        self.window.show_view(view)

    def first(self) -> None:
        """Resets navigation to the initial view and flushes the history stack."""
        view: arcade.View = self.view_history[0]
        self.window.show_view(view)
        self.view_history = []

    def run(self) -> None:
        """Starts the application's main event loop."""
        arcade.run()

    def display(self, view: arcade.View) -> None:
        """Pushes a new view onto the history stack and renders it.

        Args:
            view: The view instance to be displayed.
        """
        self.view_history.append(view)
        self.window.show_view(view)

    def hide(self) -> None:
        """Hides the currently active view."""
        self.window.hide_view()
