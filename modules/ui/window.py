import arcade
from modules.data import data
from typing import List


class Window:
    """
    Manages the main application window and view navigation history for LogicBox.
    """

    def __init__(self) -> None:
        """
        Initialize the Window class, setting up dimensions, title, and the arcade window.
        """
        # Retrieve window dimensions from configuration module
        self.width: int = data.WINDOW_WIDTH
        self.height: int = data.WINDOW_HEIGHT
        self.title: str = "LogicBox"

        # Initialize the underlying arcade window with specified settings
        # The update/draw rates correspond to approximately 60 FPS (1/60 seconds)
        self.window: arcade.Window = arcade.Window(
            self.width,
            self.height,
            self.title,
            fullscreen=data.WINDOW_FULLSCREEN,
            update_rate=0.01666666666666666666666666666,
            draw_rate=0.01666666666666666666666666666,
        )

        # Track history of views for navigation
        self.view_history: List[arcade.View] = []

    def back(self) -> None:
        """
        Navigate to the previous view in the history stack.

        Removes the current view from history and sets the window to the
        previous view.
        """
        self.view_history.pop()  # Remove current view
        view: arcade.View = self.view_history[-1]  # Peek at the last view
        self.window.show_view(view)  # Display the previous view

    def first(self) -> None:
        """
        Navigate back to the initial view and clear the history.
        """
        view: arcade.View = self.view_history[0]  # Get the initial view
        self.window.show_view(view)  # Display it
        self.view_history = []  # Clear history list

    def run(self) -> None:
        """
        Start the arcade main event loop.
        """
        arcade.run()  # Enter the main execution loop

    def display(self, view: arcade.View) -> None:
        """
        Set a new view and add it to the navigation history.

        Parameters:
        - view: The arcade.View object to be displayed.
        """
        self.view_history.append(view)  # Add new view to stack
        self.window.show_view(view)  # Switch window to this view

    def hide(self) -> None:
        """
        Hide the current view.
        """
        self.window.hide_view()  # Call arcade method to hide active view
