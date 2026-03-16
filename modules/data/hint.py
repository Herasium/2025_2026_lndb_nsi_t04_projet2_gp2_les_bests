from modules.data.chip import Chip


class Hint:
    """
    Represents a hint object that can be displayed to a user.

    Attributes:
        chip (Chip): The Chip object associated with this hint.
        text (str): The content of the hint.
        type (int): The display format (0: Textual, 1: Chip, 2: Both).
        id (int): Unique identifier for the hint.
    """

    def __init__(self, id: int) -> None:
        """
        Initializes the Hint object with a specific ID.

        Parameters:
        - id: The unique identifier for the hint.
        """
        # Create a Chip object with a formatted string identifier
        self.chip: Chip = Chip(f"hint_chip_{id}")

        # Set default text content
        self.text: str = "Default Hint"

        # Initialize display type: 0: Textual, 1: Chip, 2: Both
        self.type: int = 0

        # Store the provided ID
        self.id: int = id
