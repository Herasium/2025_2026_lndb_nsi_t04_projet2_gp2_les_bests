from typing import Dict


class English:
    """Class containing English localization strings for the application."""

    def __init__(self) -> None:
        """Initialize the English dictionary with tutorial and UI strings.

        Returns:
            None
        """
        # Dictionary mapping menu keys to their corresponding English text strings
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
        """Retrieve a specific translation string based on the menu and key.

        Parameters:
        - menu (str): The name of the dictionary attribute to search (e.g., 'tutorial').
        - key (str): The specific key within that dictionary.

        Returns:
        - str: The translated string if found, or an error message if not.
        """
        # Check if the requested menu name exists as an attribute of the class
        if menu in self.__dict__:
            # Check if the specific key exists within the selected menu dictionary
            if key in self.__dict__[menu]:
                return self.__dict__[menu][key]  # Return the found translation
            else:
                # Fallback message for missing keys
                return f"Key '{key}' not found in menu '{menu}'"
        else:
            # Fallback message for missing menu attributes
            return f"Menu '{menu}' not found"


class French:
    """Class containing French localization strings for the application."""

    def __init__(self) -> None:
        """Initialize the French dictionary with tutorial and UI strings.

        Returns:
            None
        """
        # Dictionary mapping menu keys to their corresponding French text strings
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
        """Retrieve a specific translation string based on the menu and key.

        Parameters:
        - menu (str): The name of the dictionary attribute to search (e.g., 'tutorial').
        - key (str): The specific key within that dictionary.

        Returns:
        - str: The translated string if found, or an error message if not.
        """
        # Check if the requested menu name exists as an attribute of the class
        if menu in self.__dict__:
            # Check if the specific key exists within the selected menu dictionary
            if key in self.__dict__[menu]:
                return self.__dict__[menu][key]  # Return the found translation
            else:
                # Fallback message in French for missing keys
                return f"Clé '{key}' non trouvée dans menu '{menu}'."
        else:
            # Fallback message in French for missing menu attributes
            return f"Menu '{menu}' non trouvé."
