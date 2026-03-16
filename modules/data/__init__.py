from typing import Any, Dict, List, Optional, Union
from modules.data.language import English, French


class COLORS:
    """Namespace for color hex codes used in the application."""

    VALUE_ON: str = "DC2626"
    VALUE_OFF: str = "D9D9D9"


class ImageBuffer:
    """Manages a collection of gate textures and their completion states."""

    def __init__(self) -> None:
        """Initialize an empty image buffer."""
        self.buffer: Dict[str, Dict[str, Any]] = {}

    def add_gate_type(self, id: str) -> None:
        """
        Register a new gate type in the buffer.

        Parameters:
        - id: Unique identifier for the gate type.
        """
        # Create a dictionary entry for the gate with default incomplete status
        self.buffer[id] = {"complete": False, "textures": {}}

    def add_texture(self, id: str, texture_id: str, texture: Any) -> None:
        """
        Store a texture for a specific gate.

        Parameters:
        - id: Gate identifier.
        - texture_id: Unique identifier for the texture.
        - texture: The texture object to store.
        """
        self.buffer[id]["textures"][texture_id] = texture

    def get_texture(self, id: str, texture_id: str) -> Union[Any, bool]:
        """
        Retrieve a texture from the buffer.

        Parameters:
        - id: Gate identifier.
        - texture_id: Unique identifier for the texture.

        Returns:
        - The texture object if found, otherwise False.
        """
        if texture_id in self.buffer[id]["textures"]:
            return self.buffer[id]["textures"][texture_id]
        else:
            return False  # Return False if texture does not exist

    def complete_gate(self, id: str) -> None:
        """
        Mark a gate as complete.

        Parameters:
        - id: Gate identifier.
        """
        self.buffer[id]["complete"] = True

    def is_complete_gate(self, id: str) -> bool:
        """
        Check if a gate is marked as complete.

        Parameters:
        - id: Gate identifier.

        Returns:
        - True if complete, False otherwise.
        """
        return self.buffer[id]["complete"]


class LevelButtonsBuffer:
    """Manages storage for level button images."""

    def __init__(self) -> None:
        """Initialize an empty level button buffer."""
        self.buffer: Dict[str, Any] = {}

    def get(self, id: str) -> Any:
        """
        Retrieve a button image by ID.

        Parameters:
        - id: Level button identifier.

        Returns:
        - The associated image data.
        """
        return self.buffer[id]

    def set(self, id: str, image: Any) -> None:
        """
        Set or update a button image.

        Parameters:
        - id: Level button identifier.
        - image: The image data to store.
        """
        self.buffer[id] = image


class Data:
    """Central data repository for application settings, states, and assets."""

    def __init__(self) -> None:
        """Initialize global settings, buffers, and language configurations."""
        self.WINDOW_WIDTH: int = 1920
        self.WINDOW_HEIGHT: int = 1080
        self.WINDOW_FULLSCREEN: bool = True
        self.UI_EDITOR_GRID_SIZE: int = 27
        self.VERSION: int = 200
        self.COLORS = COLORS
        self.IMAGE: ImageBuffer = ImageBuffer()
        self.LEVEL_BUTTONS: LevelButtonsBuffer = LevelButtonsBuffer()

        # Dictionaries to hold game state data
        self.loaded_chips: Dict[str, Any] = {}
        self.loaded_levels: Dict[str, Any] = {}

        self.window: Optional[Any] = None
        self.level_colors: List[str] = ["green", "yellow", "orange", "red"]
        self.categories: List[str] = [
            "Fondamentals of logic",
            "Some basic gates",
            "Some NANDic gates",
            "Triple inputs gates",
            "Triple NANDuts gates",
            "Basics of arithmetic",
        ]

        # Initialize language based on current selection
        self.current_lang: str = "en"
        if self.current_lang == "en":
            self.language = English()
        else:
            self.language = French()


# Instantiate the global data object
data: Data = Data()
