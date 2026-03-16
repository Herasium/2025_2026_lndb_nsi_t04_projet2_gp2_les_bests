# Imports
# -------------------------------------------------
from modules.data import data  # Global Shared Data
import datetime
# -------------------------------------------------

class Logger:
    """
    Logger: Basic logger to help debug and display critical informations.
    Display messages with a color code for easy debugging.
    Takes as input the name of the process (Loader, Main...).
    """

    def __init__(self, name: str):
        """
        Initialize the Logger with the given process name.
        """
        self.name = name

        self.levels = [
            "DEBUG",  # Low level info, often temporary
            "INFO",  # Basic informations, startup notice, version etc..
            "SUCCESS",  # Launch of a new part of the code (MainMenu etc..)
            "WARNING",  # Non critical errors, todos...
            "ERROR"  # Fatal errors, that will result in a game crash / freeze.
        ]

        self.colors = [
            "\033[0m",  # Default Debug
            "\033[36m",  # Cyan Info
            "\033[92m",  # Bright Green Success
            "\033[33m",  # Yellow Warning
            "\033[31m",  # Red Error
        ]
        """ANSI Color coding for the messages."""

        self.history = []  # Saved message history, to save in file if needed.

    def _header(self, level: int) -> str:
        """
        First part of the message, containing the severity and the color,
        as well as the process that sent the message and a timestamp for good measure.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S.%f")
        header = f"{self.colors[level]}LogicBox v.{data.VERSION} | {self.name} | {timestamp} | {self.levels[level]} | "
        # Result Example: LogicBox v.136 | Loader | 17:12:55.200927 | SUCCESS | (all in bright green)
        return header

    def debug(self, message: str) -> None:
        """
        Log a debug message.
        """
        data = f"{self._header(0)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)

    def print(self, message: str) -> None:
        """
        Log an info message.
        """
        data = f"{self._header(1)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)

    def info(self, message: str) -> None:
        """
        Log an info message.
        """
        data = f"{self._header(1)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)

    def success(self, message: str) -> None:
        """
        Log a success message.
        """
        data = f"{self._header(2)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)

    def warning(self, message: str) -> None:
        """
        Log a warning message.
        """
        data = f"{self._header(3)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)

    def error(self, message: str) -> None:
        """
        Log an error message.
        """
        data = f"{self._header(4)}{message}{self.colors[0]}"
        self.history.append(data)
        print(data)
