"""Provides the base Node class for UI toolbox elements."""

from typing import Any
from modules.ui.toolbox.entity import Entity


class Node:
    """Represents a structural element within the UI toolbox system."""

    def __init__(self, id: Any) -> None:
        """Initializes the node with a unique identifier and default state.

        Args:
            id: The unique identifier to be assigned to this node.
        """
        self.entity: Entity = Entity()
        self.type: str = "DefaultNode"
        self.id: Any = id
        self._name: str = f"{self.type} ({self.id})"

    def draw(self) -> None:
        """Renders the node to the UI."""
        self.entity.draw()
