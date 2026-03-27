from typing import Any, Dict, List, Optional, Union
from modules.data.language import English, French
import os
import json

"""Fournit les structures de données et la gestion d'état pour les ressources et la configuration de l'application."""


class COLORS:
    """Définit les constantes de la palette de couleurs au format hexadécimal."""

    VALUE_ON: str = "DC2626"
    VALUE_OFF: str = "D9D9D9"


class ImageBuffer:
    """Gère le stockage et le suivi de l'état d'achèvement des textures liées aux portes logiques."""

    def __init__(self) -> None:
        """Initialise un tampon de ressources vide."""
        self.buffer: Dict[str, Dict[str, Any]] = {}

    def add_gate_type(self, id: str) -> None:
        """Enregistre une nouvelle catégorie de porte dans le tampon.

        Args:
            id: Identifiant du type de porte.
        """
        self.buffer[id] = {"complete": False, "textures": {}}

    def add_texture(self, id: str, texture_id: str, texture: Any) -> None:
        """Stocke un objet de texture pour une porte spécifique.

        Args:
            id: Identifiant de la porte.
            texture_id: Identifiant de la texture.
            texture: La ressource à stocker.
        """
        self.buffer[id]["textures"][texture_id] = texture

    def get_texture(self, id: str, texture_id: str) -> Union[Any, bool]:
        """Récupère une texture spécifique depuis le tampon.

        Args:
            id: Identifiant de la porte.
            texture_id: Identifiant de la texture.

        Returns:
            L'objet texture si trouvé, sinon False.
        """
        if texture_id in self.buffer[id]["textures"]:
            return self.buffer[id]["textures"][texture_id]
        return False

    def complete_gate(self, id: str) -> None:
        """Marque une porte spécifique comme terminée.

        Args:
            id: Identifiant de la porte.
        """
        self.buffer[id]["complete"] = True

    def is_complete_gate(self, id: str) -> bool:
        """Vérifie si une porte a été marquée comme terminée.

        Args:
            id: Identifiant de la porte.

        Returns:
            True si la porte est marquée comme terminée, sinon False.
        """
        return self.buffer[id]["complete"]


class LevelButtonsBuffer:
    """Gère le stockage et la récupération des éléments d'interface de sélection de niveau."""

    def __init__(self) -> None:
        """Initialise un tampon de stockage vide pour les boutons."""
        self.buffer: Dict[str, Any] = {}

    def get(self, id: str) -> Any:
        """Récupère les données d'un bouton.

        Args:
            id: Identifiant du bouton de niveau.

        Returns:
            Les données d'image du bouton associé.
        """
        return self.buffer[id]

    def set(self, id: str, image: Any) -> None:
        """Stocke ou met à jour les données d'un bouton.

        Args:
            id: Identifiant du bouton de niveau.
            image: Données d'image à stocker.
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

        self.back = 65307  # Échap
        self.input_toggle = 101  # E
        self.chip_save = 115  # S
        self.gate_delete = 65288  # Supprimer


class Data:
    """Répertoire principal pour l'état global de l'application, les paramètres et les registres d'objets."""

    def __init__(self) -> None:
        """Initialise les configurations par défaut de l'application et les registres de données."""
        self.WINDOW_WIDTH: int = 1920
        self.WINDOW_HEIGHT: int = 1080
        self.WINDOW_FULLSCREEN: bool = True
        self.WINDOW_FRAMERATE: int = 60
        self.UI_EDITOR_GRID_SIZE: int = 27
        self.VERSION: int = 300
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
        self.level_colors: List[str] = ["blue","green", "yellow", "orange", "red","purple","black"]
        self.categories: List[str] = [
            "Fondamentals of logic",
            "Some basic gates",
            "Triple inputs gates",
            "Basics of arithmetic",
            "The more the better",
            "Divide and conquer",
            "The END",
            "Some NANDic gates",
            "Triple NANDuts gates",
            "NANDics of arithmetic",
            "The more the NANDier"
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