from typing import Any, Dict, List, Optional, Union
from modules.data.language import English, French
import os
import json

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


class Audio:
    def __init__(self) -> None:
        self.global_volume = 100
        self.music_volume = 100
        self.sfx_volume = 100
        self.mute = False


class KeyBinds:

    def __init__(self) -> None:

        self.back = 65307  # Esc
        self.input_toggle = 101  # E
        self.chip_save = 115  # S
        self.gate_delete = 65288  # Delete


class Data:
    """Main repository for application global state, settings, and object registries."""

    def __init__(self) -> None:
        """Initializes default application configurations and data registries."""
        self.WINDOW_WIDTH: int = 1920
        self.WINDOW_HEIGHT: int = 1080
        self.WINDOW_FULLSCREEN: bool = False
        self.WINDOW_FRAMERATE: int = 60
        self.UI_EDITOR_GRID_SIZE: int = 27
        self.VERSION: int = 208
        self.COLORS = COLORS
        self.IMAGE: ImageBuffer = ImageBuffer()
        self.LEVEL_BUTTONS: LevelButtonsBuffer = LevelButtonsBuffer()
        self.MOUSE_SENSI = 40
        self.LOGGER_MIN = 1
        self.current_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../")
        )
        self.audio = Audio()
        self.keys = KeyBinds()

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
            "The more the better",
            "Divide and conquer"
        ]

        self.current_lang: str = "en"
        if self.current_lang == "en":
            self.language = English()
        else:
            self.language = French()

    def save(self) -> None:
        preferences = {
            "window_fullscreen": self.WINDOW_FULLSCREEN,
            "window_framerate": self.WINDOW_FRAMERATE,
            "mouse_sensitivity": self.MOUSE_SENSI,
            "audio": {
                "global_volume": self.audio.global_volume,
                "music_volume": self.audio.music_volume,
                "sfx_volume": self.audio.sfx_volume,
                "mute": self.audio.mute,
            },
            "keybinds": {
                "back": self.keys.back,
                "input_toggle": self.keys.input_toggle,
                "chip_save": self.keys.chip_save,
                "gate_delete": self.keys.gate_delete,
            },
            "current_lang": self.current_lang,
        }

        preferences_file_path = os.path.join(self.current_path, "preferences.json")
        with open(preferences_file_path, "w") as preferences_file:
            json.dump(preferences, preferences_file, indent=4)

    def load(self) -> None:
        preferences_file_path = os.path.join(self.current_path, "preferences.json")
        if os.path.exists(preferences_file_path):
            with open(preferences_file_path, "r") as preferences_file:
                preferences = json.load(preferences_file)
                self.WINDOW_FULLSCREEN = preferences.get(
                    "window_fullscreen", self.WINDOW_FULLSCREEN
                )
                self.WINDOW_FRAMERATE = preferences.get(
                    "window_framerate", self.WINDOW_FRAMERATE
                )
                self.MOUSE_SENSI = preferences.get(
                    "mouse_sensitivity", self.MOUSE_SENSI
                )
                self.audio.global_volume = preferences["audio"].get(
                    "global_volume", self.audio.global_volume
                )
                self.audio.music_volume = preferences["audio"].get(
                    "music_volume", self.audio.music_volume
                )
                self.audio.sfx_volume = preferences["audio"].get(
                    "sfx_volume", self.audio.sfx_volume
                )
                self.audio.mute = preferences["audio"].get("mute", self.audio.mute)
                self.keys.back = preferences["keybinds"].get("back", self.keys.back)
                self.keys.input_toggle = preferences["keybinds"].get(
                    "input_toggle", self.keys.input_toggle
                )
                self.keys.chip_save = preferences["keybinds"].get(
                    "chip_save", self.keys.chip_save
                )
                self.keys.gate_delete = preferences["keybinds"].get(
                    "gate_delete", self.keys.gate_delete
                )
                self.current_lang = preferences.get("current_lang", self.current_lang)
                if self.current_lang == "en":
                    self.language = English()
                else:
                    self.language = French()


data: Data = Data()
