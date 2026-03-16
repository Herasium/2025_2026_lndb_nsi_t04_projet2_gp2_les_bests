"""Provides localization classes for application UI strings."""

from typing import Dict


class English:
    """Stores and retrieves English localization strings."""

    def __init__(self) -> None:
        """Initializes the tutorial string repository."""
        self.tutorial: Dict[str, str] = {
            "button_1": "-> How to play ?",
            "button_2": "-> Keyboard commands",
            "button_3": "-> INPUT",
            "button_4": "-> OUTPUT",
            "button_5": "-> AND",
            "button_6": "-> NOT",
            "button_7": "-> OR",
            "button_8": "-> NAND",
            "button_9": "-> NOR",
            "button_10": "-> XOR",
            "button_11": "-> CLOCK",
            "button_12": "-> PASS",
            "title_1": "Rules",
            "title_2": "Logic gates",
            "button_01": "Drag gates from the hotbar\nto the playground. You can click on the output port\nof a gate to create a wire \nand then on the input port\nof another gate to connect them.",
            "button_02": "def",
        }

    def get(self, menu: str, key: str) -> str:
        """Retrieves a translation string by category and identifier.

        Args:
            menu: The attribute name containing the dictionary to search.
            key: The specific identifier for the desired string.

        Returns:
            The corresponding string if found, otherwise an error message.
        """
        if menu in self.__dict__:
            if key in self.__dict__[menu]:
                return self.__dict__[menu][key]
            else:
                return f"Key '{key}' not found in menu '{menu}'"
        else:
            return f"Menu '{menu}' not found"


class French:
    """Stores and retrieves French localization strings."""

    def __init__(self) -> None:
        """Initializes the tutorial string repository."""
        self.tutorial: Dict[str, str] = {
            "button_1": "-> Comment jouer ?",
            "button_2": "-> Commandes clavier",
            "button_3": "-> INPUT",
            "button_4": "-> OUTPUT",
            "button_5": "-> AND",
            "button_6": "-> NOT",
            "button_7": "-> OR",
            "button_8": "-> NAND",
            "button_9": "-> NOR",
            "button_10": "-> XOR",
            "button_11": "-> CLOCK",
            "button_12": "-> PASS",
            "title_1": "Règles",
            "title_2": "Portes logiques",
            "button_01": "zyx",
            "button_02": "wvu",
        }

    def get(self, menu: str, key: str) -> str:
        """Retrieves a translation string by category and identifier.

        Args:
            menu: The attribute name containing the dictionary to search.
            key: The specific identifier for the desired string.

        Returns:
            The corresponding string if found, otherwise an error message.
        """
        if menu in self.__dict__:
            if key in self.__dict__[menu]:
                return self.__dict__[menu][key]
            else:
                return f"Clé '{key}' non trouvée dans menu '{menu}'."
        else:
            return f"Menu '{menu}' non trouvé."
