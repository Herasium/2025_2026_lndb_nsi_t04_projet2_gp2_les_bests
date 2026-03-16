"""Provides mechanisms for defining and managing user interface hint elements."""

from modules.data.chip import Chip


class Hint:
    """Represents a UI hint configured for specific display formats.

    Attributes:
        chip: The associated data representation for chip-based display.
        text: The primary string content displayed to the user.
        type: The rendering mode where 0 is text-only, 1 is chip-only, and 2 is combined.
        id: The unique identifier for this instance.
    """

    def __init__(self, id: int) -> None:
        """Initializes the hint instance with a default configuration.

        Args:
            id: The unique identifier used to generate the internal chip reference.
        """
        self.chip: Chip = Chip(f"hint_chip_{id}")
        self.text: str = "Default Hint"
        self.type: int = 0
        self.id: int = id
