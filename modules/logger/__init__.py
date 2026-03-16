# Imports
# -------------------------------------------------
from modules.data import data  # Global Shared Data
import datetime
from typing import List

# -------------------------------------------------


class Logger:
    """
    Logger: Basic logger to help debug and display critical information.
    Displays messages with a color code for easy debugging.
    Takes as input the name of the process (Loader, Main...).

    Attributes:
    - name (str): The name of the process using the logger.
    - levels (List[str]): List of available logging severity levels.
    - colors (List[str]): List of ANSI escape sequences for color coding.
    - history (List[str]): A list of all logged messages for the current session.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize the Logger with the given process name and set up logging levels.

        Parameters:
        - name (str): The name of the process or module (e.g., 'Main', 'Loader').

        Returns:
        - None
        """
        self.name: str = name

        # Define logging level labels
        self.levels: List[str] = [
            "DEBUG",  # Low level info, often temporary
            "INFO",  # Basic information, startup notice, version etc..
            "SUCCESS",  # Launch of a new part of the code (MainMenu etc..)
            "WARNING",  # Non critical errors, todos...
            "ERROR",  # Fatal errors that result in a game crash / freeze.
        ]

        # Define ANSI color codes corresponding to the levels above
        self.colors: List[str] = [
            "\033[0m",  # Default (Reset)
            "\033[36m",  # Cyan Info
            "\033[92m",  # Bright Green Success
            "\033[33m",  # Yellow Warning
            "\033[31m",  # Red Error
        ]

        # Initialize an empty list to store logged strings
        self.history: List[str] = []

    def _header(self, level: int) -> str:
        """
        Generate the first part of the message, containing severity, color,
        process name, and timestamp.

        Parameters:
        - level (int): The index representing the logging level in self.levels.

        Returns:
        - str: A formatted string containing the ANSI color, version, name, and timestamp.
        """
        # Fetch current date and time with microsecond precision
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S.%f")

        # Construct the prefix string using the global data versioning and current level details
        header: str = (
            f"{self.colors[level]}LogicBox v.{data.VERSION} | {self.name} | {timestamp} | {self.levels[level]} | "
        )

        return header

    def debug(self, message: str) -> None:
        """
        Log a debug message (lowest severity).

        Parameters:
        - message (str): The content of the log entry.

        Returns:
        - None
        """
        # Format: [Header][Message][Reset Color]
        log_data: str = f"{self._header(0)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def print(self, message: str) -> None:
        """
        Alias for log an info message.

        Parameters:
        - message (str): The content of the log entry.

        Returns:
        - None
        """
        log_data: str = f"{self._header(1)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def info(self, message: str) -> None:
        """
        Log an info message (standard information).

        Parameters:
        - message (str): The content of the log entry.

        Returns:
        - None
        """
        log_data: str = f"{self._header(1)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def success(self, message: str) -> None:
        """
        Log a success message (green highlight).

        Parameters:
        - message (str): The content of the log entry.

        Returns:
        - None
        """
        log_data: str = f"{self._header(2)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def warning(self, message: str) -> None:
        """
        Log a warning message (non-fatal issue).

        Parameters:
        - message (str): The content of the log entry.

        Returns:
        - None
        """
        log_data: str = f"{self._header(3)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def error(self, message: str) -> None:
        """
        Log an error message (critical failure).

        Parameters:
        - message (str): The content of the log entry.

        Returns:
        - None
        """
        log_data: str = f"{self._header(4)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)
