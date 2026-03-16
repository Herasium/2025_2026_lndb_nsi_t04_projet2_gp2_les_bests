from typing import Any
from modules.ui.toolbox.entity import Entity


class Node:
    """Represents a basic node element within the UI toolbox.

    Attributes:
        entity (Entity): The UI entity instance associated with this node.
        type (str): The classification type of the node.
        id (Any): A unique identifier for the node.
        _name (str): The internal display name of the node.
    """

    def __init__(self, id: Any) -> None:
        """Initialize a new Node instance with a unique ID and default properties.

        Parameters:
            id (Any): The unique identifier to assign to this node.

        Returns:
            None
        """
        # Instantiate the core UI component for this node
        self.entity: Entity = Entity()

        # Set the default classification type
        self.type: str = "DefaultNode"

        # Assign the unique identifier provided during instantiation
        self.id: Any = id

        # Construct the internal name using a formatted string of type and ID
        self._name: str = f"{self.type} ({self.id})"

    def draw(self) -> None:
        """Render the node by invoking the draw method of its associated entity.

        Parameters:
            None

        Returns:
            None
        """
        # Delegate the rendering logic to the internal entity object
        self.entity.draw()
