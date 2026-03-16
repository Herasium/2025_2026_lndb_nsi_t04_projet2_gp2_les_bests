from modules.data import data
import datetime
from typing import List

"""Provides a centralized logging utility with ANSI color-coded output."""


class Logger:
    """Handles formatted console logging for application processes.

    Attributes:
        name: The identifier of the process using this instance.
        levels: Severity classification labels.
        colors: ANSI escape sequences for terminal output styling.
        history: Captured log entries from the current session.
    """

    def __init__(self, name: str) -> None:
        """Initializes the Logger instance.

        Args:
            name: The process or module identifier.
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
        """Constructs a standardized prefix for log messages.

        Args:
            level: The index corresponding to the severity level.

        Returns:
            A formatted string containing versioning, process name, timestamp, and severity.
        """
        timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S.%f")

        header: str = (
            f"{self.colors[level]}LogicBox v.{data.VERSION} | {self.name} | {timestamp} | {self.levels[level]} | "
        )

        return header

    def debug(self, message: str) -> None:
        """Logs a message with DEBUG severity.

        Args:
            message: The content to be logged.
        """
        log_data: str = f"{self._header(0)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def print(self, message: str) -> None:
        """Logs a message with INFO severity as a default alias.

        Args:
            message: The content to be logged.
        """
        log_data: str = f"{self._header(1)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def info(self, message: str) -> None:
        """Logs a message with INFO severity.

        Args:
            message: The content to be logged.
        """
        log_data: str = f"{self._header(1)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def success(self, message: str) -> None:
        """Logs a message with SUCCESS severity.

        Args:
            message: The content to be logged.
        """
        log_data: str = f"{self._header(2)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def warning(self, message: str) -> None:
        """Logs a message with WARNING severity.

        Args:
            message: The content to be logged.
        """
        log_data: str = f"{self._header(3)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)

    def error(self, message: str) -> None:
        """Logs a message with ERROR severity.

        Args:
            message: The content to be logged.
        """
        log_data: str = f"{self._header(4)}{message}{self.colors[0]}"
        self.history.append(log_data)
        print(log_data)
