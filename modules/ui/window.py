"""Provides window management and view navigation state for the LogicBox application."""

import arcade
from modules.data import data
from typing import List
from modules.logger import Logger

logger: Logger = Logger("Window")


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
            update_rate=1 / data.WINDOW_FRAMERATE,
            draw_rate=1 / data.WINDOW_FRAMERATE,
        )

        self.view_history: List[arcade.View] = []

    def back(self) -> None:
        """Navigates to the previous view in the history stack."""
        if len(self.view_history) < 2:
            logger.warning("No view to go back to. Doing Nothing.")
            return
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
