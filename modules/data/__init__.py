from typing import Any, Dict, List, Optional, Union
from modules.data.language import English, French

"""Provides data structures and state management for application assets and configuration."""


class COLORS:
    """Defines color palette constants in hexadecimal format."""

    VALUE_ON: str = "DC2626"
    VALUE_OFF: str = "D9D9D9"


class ImageBuffer:
    """Handles storage and completion tracking for gate-related texture assets."""

    def __init__(self) -> None:
        """Initializes an empty asset buffer."""
        self.buffer: Dict[str, Dict[str, Any]] = {}

    def add_gate_type(self, id: str) -> None:
        """Registers a new gate category in the buffer.

        Args:
            id: Identifier for the gate type.
        """
        self.buffer[id] = {"complete": False, "textures": {}}

    def add_texture(self, id: str, texture_id: str, texture: Any) -> None:
        """Stores a texture object for a specific gate.

        Args:
            id: Gate identifier.
            texture_id: Identifier for the texture.
            texture: The asset to store.
        """
        self.buffer[id]["textures"][texture_id] = texture

    def get_texture(self, id: str, texture_id: str) -> Union[Any, bool]:
        """Retrieves a specific texture from the buffer.

        Args:
            id: Gate identifier.
            texture_id: Identifier for the texture.

        Returns:
            The texture object if found, otherwise False.
        """
        if texture_id in self.buffer[id]["textures"]:
            return self.buffer[id]["textures"][texture_id]
        return False

    def complete_gate(self, id: str) -> None:
        """Marks a specific gate as complete.

        Args:
            id: Gate identifier.
        """
        self.buffer[id]["complete"] = True

    def is_complete_gate(self, id: str) -> bool:
        """Checks if a gate has been marked as complete.

        Args:
            id: Gate identifier.

        Returns:
            True if the gate is marked complete, otherwise False.
        """
        return self.buffer[id]["complete"]


class LevelButtonsBuffer:
    """Manages storage and retrieval for level selection interface elements."""

    def __init__(self) -> None:
        """Initializes an empty storage buffer for buttons."""
        self.buffer: Dict[str, Any] = {}

    def get(self, id: str) -> Any:
        """Retrieves button data.

        Args:
            id: Level button identifier.

        Returns:
            The associated button image data.
        """
        return self.buffer[id]

    def set(self, id: str, image: Any) -> None:
        """Stores or updates button data.

        Args:
            id: Level button identifier.
            image: Image data to be stored.
        """
        self.buffer[id] = image


class Data:
    """Main repository for application global state, settings, and object registries."""

    def __init__(self) -> None:
        """Initializes default application configurations and data registries."""
        self.WINDOW_WIDTH: int = 1920
        self.WINDOW_HEIGHT: int = 1080
        self.WINDOW_FULLSCREEN: bool = True
        self.UI_EDITOR_GRID_SIZE: int = 27
        self.VERSION: int = 208
        self.COLORS = COLORS
        self.IMAGE: ImageBuffer = ImageBuffer()
        self.LEVEL_BUTTONS: LevelButtonsBuffer = LevelButtonsBuffer()
        self.MOUSE_SENSI = 40

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
            "The more the better"
        ]

        self.current_lang: str = "en"
        if self.current_lang == "en":
            self.language = English()
        else:
            self.language = French()


data: Data = Data()
