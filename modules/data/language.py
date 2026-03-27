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
            "button_5": "-> NOT",
            "button_6": "-> AND",
            "button_7": "-> OR",
            "button_8": "-> NAND",
            "button_9": "-> NOR",
            "button_10": "-> XOR",
            "button_11": "-> CLOCK",
            "button_12": "-> PASS",
            "button_13": "-> ON",
            "button_14": "-> BREAKER",
            "button_15": "-> MAKER",
            "title_1": "Rules",
            "title_2": "Logic gates",
            "title_3": "Logic gates 8 bits",
            "button_01": "Drag gates from the hotbar to \n\nthe playground. You can click on \n\nthe output port of a gate to create \n\na wire and then on the input port \n\nof another gate to connect them.",
            "button_02": "Escape : back \n\nE : change the value of an input \n\n(between 0 and 1) \n\nBackslash : delete \n\nMiddle click : move the camera \n\nS : save \n\nF4 : emergency shutdown",
            "button_03": "INPUT is your signal source. It \n\nis permanently placed at the \n\nbeginning of a program. You can \n\nclick on it to manually switch its \n\nstate between 0 (off) and 1 (on).",
            "button_04": "OUTPUT closes a program; it's the \n\none that sends the signal back. \n\nConnect a cable to its input port. \n\nIt will light up green if it \n\nreceives a signal 1 and remain red \n\nfor a signal 0.",
            "button_05": "NOT : \n\nConnect an input to this component \n\nto reverse the logic. If you send \n\na signal, it cuts it off at the \n\noutput; if you don't send it any \n\nsignal, it returns 1.",
            "button_06": "AND : \n\nConnect two cables to the input \n\nports on the left. The gate will \n\nonly transmit a signal to the \n\noutput if both input cables carry \n\na signal.",
            "button_07": "OR : \n\nConnect your inputs. The door will \n\nreturn a signal as soon as at least \n\none of the input ports receives a \n\nsignal 1.",
            "button_08": "NAND : \n\nThis gate functions like an AND \n\ngate, but with an inverted output. \n\nIt outputs a constant 1 signal, \n\nexcept when all its inputs are \n\nactivated.",
            "button_09": "NOR : \n\nThis gate turns off its output \n\n(signal at 0) as soon as one of its \n\ninputs is 1. It only allows \n\nsignal 1 to pass if both of its \n\ninputs are at 0.",
            "button_010": "XOR : \n\nConnect two sources. The output \n\nwill only go to 1 if the two input \n\nsignals are different (one at 1, \n\nthe other at 0).",
            "button_011": "CLOCK : \n\nOnce installed, this gate \n\nautomatically generates a signal \n\nalternating between 0 and 1 every \n\nsecond. Regardless of the inputs, \n\nthe signal it outputs depends \n\nsolely on the alternation each \n\nsecond.",
            "button_012": "PASS : \n\nUse this gate to extend a \n\nconnection or isolate a part of the \n\ncircuit. It returns the incoming \n\nsignal without any modification.",
            "button_013": "ON plays the same role as INPUT. \n\nHowever, the values ​​of ON do not \n\nvary; it sends a continuous \n\nsignal (1).",
            "button_014": "BREAKER: \n\nThis module acts as a safety \n\nand diagnostic switch. It analyzes \n\nthe incoming signal and cuts \n\noff transmission (output to 0) \n\nto isolate a section of the \n\ncircuit. Use it to test the \n\nresistance of your logic.",
            "button_015": "MAKER: \n\nThis is the final production \n\nmodule. Connect your processed \n\nsignals to its input port. It \n\nconverts the incoming stream into a \n\nconcrete result and only transmits \n\na validation signal if it receives \n\na stable 1 signal.",
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
            "button_5": "-> NOT",
            "button_6": "-> AND",
            "button_7": "-> OR",
            "button_8": "-> NAND",
            "button_9": "-> NOR",
            "button_10": "-> XOR",
            "button_11": "-> CLOCK",
            "button_12": "-> PASS",
            "button_13": "-> ON",
            "button_14": "-> BREAKER",
            "button_15": "-> MAKER",
            "title_1": "Règles",
            "title_2": "Portes logiques",
            "title_3": "Logic gates 8 bits",
            "button_01": "Faites glisser les portes depuis la barre d'accès vers l'aire de jeu. Vous pouvez cliquer sur le port de sortie d'une porte pour créer un câble, puis sur le port d'entrée d'une autre porte pour les connecter.",
            "button_02": "wvu",
            "button_03": "INPUT est votre source de signal. \n\nElle se place en permanance au \n\ndébut d'un programme. Vous pouvez \n\ncliquer dessus pour basculer \n\nmanuellement son état entre 0 \n\n(éteint) et 1 (allumé).",
            "button_04": "OUTPUT ferme un programme, c'est \n\nelle qui renvoie le signal. \n\nConnectez un câble à son port \n\nd'entrée. Elle s'illuminera en vert \n\nsi elle reçoit un signal 1 et \n\nrestera rouge pour un signal 0.",
            "button_05": "NOT : \n\nConnectez une entrée à ce composant \n\npour inverser la logique. Si vous \n\nenvoyez un signal, il le coupe en \n\nsortie, si vous ne lui partagez \n\naucun signal, il renvoie 1.",
            "button_06": "AND : \n\nReliez deux câbles aux ports \n\nd'entrée à gauche. La porte ne \n\ntransmettra un signal à la sortie \n\nque si les deux câbles d'entrée \n\ntransportent un signal 1.",
            "button_07": "OR : \n\nConnectez vos entrées. La porte \n\nretournera un signal dès qu'au \n\nmoins un des ports d'entrée reçoit \n\nun signal 1.",
            "button_08": "NAND : \n\nCette porte fonctionne comme une \n\nAND, mais avec une sortie inversée. \n\nElle émet un signal 1 en \n\npermanence, sauf quand toutes ses \n\nentrées sont activées.",
            "button_09": "NOR : \n\nCette porte éteint sa sortie \n\n(signal à 0) dès qu'une de ses \n\nentrées est 1. Elle ne laisse \n\npasser le signal 1 que si ses deux \n\nentrées sont à 0.",
            "button_010": "XOR : \n\nConnectez deux sources. La sortie \n\npassera à 1 uniquement si les deux \n\nsignaux d'entrée sont différents \n\n(l'un à 1, l'autre à 0).",
            "button_011": "CLOCK : \n\nUne fois placée, cette porte génère \n\nautomatiquement un signal alternant \n\nentre 0 et 1 toutes les secondes. \n\nQu'importe ces entrées, le signal \n\nqu'elle renvoie dépends uniquement \n\nde l'alternance chaque seconde.",
            "button_012": "PASS : \n\nUtilisez cette porte pour prolonger \n\nune connexion ou isoler une partie \n\ndu circuit. Il renvoie le signal \n\nentrant sans aucune modification.",
            "button_013": "ON tient le même role que INPUT. \n\nCependant, les valeurs de ON ne \n\nvarient pas, il envoie un signal en \n\ncontinu (1).",
            "button_014": "BREAKER : \n\nCe module agit comme un \n\ninterrupteur de sécurité et de \n\ndiagnostic. Il analyse le signal \n\nentrant et coupe la transmission \n\n(sortie à 0) pour isoler une \n\nsection du circuit. Utilisez-le \n\npour tester la résistance de \n\nvotre logique.",
            "button_015": "MAKER : \n\nC'est le module de production \n\nfinale. Connectez vos signaux \n\ntraités à son port d'entrée. Il \n\nconvertit le flux entrant en un \n\nrésultat concret et ne transmet un \n\nsignal de validation que s'il \n\nreçoit un signal 1 stable.",
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

# ON
# Breaker
# Maker
