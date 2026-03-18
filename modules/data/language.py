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
            "button_09": "NOR : \n\nThis gate turns off its output (signal at 0) as soon as one of its inputs is 1. It only allows signal 1 to pass if both of its inputs are at 0.",
            "button_010": "XOR : \n\nConnect two sources. The output will only go to 1 if the two input signals are different (one at 1, the other at 0).",
            "button_011": "CLOCK : \n\nOnce installed, this gate automatically generates a signal alternating between 0 and 1 every second. Regardless of the inputs, the signal it outputs depends solely on the alternation each second.",
            "button_012": "PASS : \n\nUse this gate to extend a connection or isolate a part of the circuit. It returns the incoming signal without any modification."
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
            "button_09": "NOR : \n\nCette porte éteint sa sortie (signal à 0) dès qu'une de ses entrées est 1. Elle ne laisse passer le signal 1 que si ses deux entrées sont à 0.",
            "button_010": "XOR : \n\nConnectez deux sources. La sortie passera à 1 uniquement si les deux signaux d'entrée sont différents (l'un à 1, l'autre à 0).",
            "button_011": "CLOCK : \n\nUne fois placée, cette porte génère automatiquement un signal alternant entre 0 et 1 toutes les secondes. Qu'importe ces entrées, le signal qu'elle renvoie dépends uniquement de l'alternance chaque seconde.",
            "button_012": "PASS : \n\nUtilisez cette porte pour prolonger une connexion ou isoler une partie du circuit. Il renvoie le signal entrant sans aucune modification."
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