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
            "button_01": "Drag gates from the hotbar to \n\nthe playground. You can click on \n\nthe output port of a gate to create \n\na wire and then on the input port \n\nof another gate to connect them.",
            "button_02": "def",
            "button_03": "INPUT is your signal source. It \n\nis permanently placed at the \n\nbeginning of a program. You can \n\nclick on it to manually switch its \n\nstate between 0 (off) and 1 (on).",
            "button_04": "OUTPUT closes a program; it's the one that sends the signal back. Connect a cable to its input port. It will light up green if it receives a signal 1 and remain red for a signal 0.",
            "button_05": "AND: \n\nConnect two cables to the input ports on the left. The gate will only transmit a signal to the output if both input cables carry a signal.",
            "button_06": "NOT : \n\nConnect an input to this component to reverse the logic. If you send a signal, it cuts it off at the output; if you don't send it any signal, it returns 1.",
            "button_07": "OR : \n\nConnect your inputs. The door will return a signal as soon as at least one of the input ports receives a signal 1.",
            "button_08": "NAND : \n\nThis gate functions like an AND gate, but with an inverted output. It outputs a constant 1 signal, except when all its inputs are activated.",
            "button_09": "-> NOR",
            "button_010": "-> XOR",
            "button_011": "-> CLOCK",
            "button_012": "fdref"
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
            "button_03": "INPUT est votre source de signal. Elle se place en permanance au début d'un programme. Vous pouvez cliquer dessus pour basculer manuellement son état entre 0 (éteint) et 1 (allumé).",
            "button_04": "OUPUT ferme un programme, c'est elle qui renvoie le signal. Connectez un câble à son port d'entrée. Elle s'illuminera en vert si elle reçoit un signal 1 et restera rouge pour un signal 0.",
            "button_05": "AND : \n\nReliez deux câbles aux ports d'entrée à gauche. La porte ne transmettra un signal à la sortie que si les deux câbles d'entree transportent un signal 1.",
            "button_06": "NOT : \n\nConnectez une entrée à ce composant pour inverser la logique. Si vous envoyez un signal, il le coupe en sortie, si vous ne lui partagez aucun signal, il renvoie 1.",
            "button_07": "OR : \n\nConnectez vos entrées. La porte retournera un signal dès qu'au moins un des ports d'entrée reçoit un signal 1.",
            "button_08": "NAND : \n\nCette porte fonctionne comme une AND, mais avec une sortie inversée. Elle émet un signal 1 en permanence, sauf quand toutes ses entrées sont activées.",
            "button_09": "-> NOR",
            "button_010": "-> XOR",
            "button_011": "-> CLOCK",
            "button_012": "fdref"
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


# Piskel