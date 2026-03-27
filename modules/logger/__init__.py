from modules.data import data
import datetime
from typing import List

"""Fournit un utilitaire de journalisation centralisé avec une sortie codée par couleurs ANSI."""


class Logger:
    """Gère la journalisation formatée dans la console pour les processus de l'application.

    Attributs :
        name : L'identifiant du processus utilisant cette instance.
        levels : Étiquettes de classification de la sévérité.
        colors : Séquences d'échappement ANSI pour le style de sortie du terminal.
        history : Entrées de journal capturées lors de la session actuelle.
    """

    def __init__(self, name: str) -> None:
        """Initialise l'instance du Logger.

        Args :
            name : L'identifiant du processus ou du module.
        """
        self.name: str = name

        self.levels: List[str] = [
            "DEBUG",
            "INFO",
            "SUCCESS",
            "WARNING",
            "ERROR",
        ]

        self.colors: List[str] = [
            "\033[0m",
            "\033[36m",
            "\033[92m",
            "\033[33m",
            "\033[31m",
        ]

        self.history: List[str] = []

    def _header(self, level: int) -> str:
        """Construit un préfixe standardisé pour les messages de journalisation.

        Args :
            level : L'index correspondant au niveau de sévérité.

        Returns :
            Une chaîne formatée contenant la version, le nom du processus, l'horodatage et la sévérité.
        """
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S.%f")

        header: str = (
            f"{self.colors[level]}LogicBox v.{data.VERSION} | {self.name} | {timestamp} | {self.levels[level]} | "
        )

        return header

    def debug(self, message: str) -> None:
        """Enregistre un message avec la sévérité DEBUG.

        Args :
            message : Le contenu à journaliser.
        """
        if data.LOGGER_MIN > 0:
            return
        log_data: str = f"{self._header(0)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def print(self, message: str) -> None:
        """Enregistre un message avec la sévérité INFO par défaut.

        Args :
            message : Le contenu à journaliser.
        """
        if data.LOGGER_MIN > 1:
            return
        log_data: str = f"{self._header(1)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def info(self, message: str) -> None:
        """Enregistre un message avec la sévérité INFO.

        Args :
            message : Le contenu à journaliser.
        """
        if data.LOGGER_MIN > 1:
            return
        log_data: str = f"{self._header(1)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def success(self, message: str) -> None:
        """Enregistre un message avec la sévérité SUCCESS.

        Args :
            message : Le contenu à journaliser.
        """
        if data.LOGGER_MIN > 2:
            return
        log_data: str = f"{self._header(2)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def warning(self, message: str) -> None:
        """Enregistre un message avec la sévérité WARNING.

        Args :
            message : Le contenu à journaliser.
        """
        if data.LOGGER_MIN > 2:
            return
        log_data: str = f"{self._header(3)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def error(self, message: str) -> None:
        """Enregistre un message avec la sévérité ERROR.

        Args :
            message : Le contenu à journaliser.
        """
        if data.LOGGER_MIN > 4:
            return
        log_data: str = f"{self._header(4)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)