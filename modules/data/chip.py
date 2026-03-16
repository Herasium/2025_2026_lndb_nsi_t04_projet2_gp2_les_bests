import json
import os
from typing import Dict, List, Any, Union, Optional

from modules.data import data
from modules.data.gate_index import gate_types
from modules.data.nodes.path import Path
from modules.logger import Logger
from modules.ui.toolbox.id_generator import random_id
from modules.data.custom import CustomGate

# Initialize a logger instance for the Chip class
logger: Logger = Logger("Chip")


class Chip:
    """Represents a logic chip containing gates, paths, and metadata."""

    def __init__(self, id: str) -> None:
        """Initialize a new Chip instance.

        Parameters:
        - id: A unique identifier for the chip.
        """
        self.paths: Dict[str, Path] = {}  # Map of path IDs to Path objects
        self.gates: Dict[str, Any] = {}  # Map of gate IDs to Gate/CustomGate objects
        self.id: str = id
        self.name: str = "Default Chip"
        self.type: str = "Chip"
        self.changed: bool = False  # Tracks if the chip has unsaved changes
        self.requirements: List[str] = []  # List of dependency chip IDs
        self.temp_data: Optional[Dict] = (
            None  # Buffer for data during the loading process
        )

    def copy(self) -> "Chip":
        """Create a deep copy of the current chip with a new unique ID.

        Returns:
        - Chip: A new Chip instance with identical logic but a different ID.
        """
        new: Chip = Chip("no_id")
        # Serialize current state to JSON and reload into the new instance
        new.partial_load(json.loads(self.save(no_file=True, dojson=True)))
        new.load()
        new.id = random_id()  # Assign a fresh ID to the copy
        return new

    def save(
        self, no_file: bool = False, dojson: bool = False
    ) -> Union[Dict, str, None]:
        """Save the chip state to a dictionary, JSON string, or a physical file.

        Parameters:
        - no_file: If True, prevents writing to the disk.
        - dojson: If True, returns a JSON string instead of a dictionary.

        Returns:
        - Union[Dict, str, None]: The serialized chip data or None if saved to file.
        """
        paths: Dict[str, Any] = {}
        gates: Dict[str, Any] = {}

        self.requirements = []  # Reset requirements to recalculate dependencies

        # Serialize all internal paths
        for id in self.paths:
            paths[id] = self.paths[id].save()

        # Serialize all internal gates and track dependencies
        for id in self.gates:
            gates[id] = self.gates[id].save()
            # If a gate is a Custom type, it depends on another chip
            if self.gates[id].type == "Custom":
                self.requirements.append(self.gates[id].base_chip_id)
                # Inherit requirements from the sub-chip recursively
                self.requirements += data.loaded_chips[
                    self.gates[id].base_chip_id
                ].requirements

        # Remove duplicates from the requirements list
        self.requirements = list(set(self.requirements))

        # Structure the final data object
        result: Dict[str, Any] = {
            "type": self.type,
            "name": self.name,
            "id": self.id,
            "gates": gates,
            "paths": paths,
            "version": data.VERSION,
            "requirements": self.requirements,
        }

        # Handle memory-only returns
        if no_file and not dojson:
            return result

        dump: str = json.dumps(result, indent=1)
        if dojson:
            return dump

        # File System Operations: Save to the 'saves' directory
        path: str = data.current_path
        os.makedirs(os.path.join(path, "saves"), exist_ok=True)
        file_path: str = os.path.join(os.path.join(path, "saves"), f"{self.id}.chip")

        with open(file_path, "wb") as file:
            file.write(dump.encode())

        logger.print(f"Saved {self.name}, #{self.id}")
        return None

    def partial_load(self, data: Dict[str, Any]) -> None:
        """Load basic metadata and store gate/path data into temp_data for later processing.

        Parameters:
        - data: A dictionary containing chip state and metadata.
        """
        self.type = data["type"]
        self.name = data["name"]
        self.id = data["id"]

        # Legacy version check for compatibility
        if data["version"] != "a.136":
            self.requirements = data["requirements"]

        self.temp_data = data  # Buffer data to be fully processed by load()

    def load(self) -> None:
        """Process temp_data to reconstruct gate and path objects.
        Must be called after partial_load.
        """
        if self.temp_data is None:
            logger.error("You must partial load a chip, before finishing load.")
            return

        data_map: Dict[str, Any] = self.temp_data

        # Instantiate and load gates based on their specific types
        for key in data_map["gates"]:
            gate = data_map["gates"][key]
            if gate["type"] in ["Gate", "Complex"]:
                new = gate_types[gate["gate"]]("default_id")
            elif gate["type"] == "Custom":
                new = CustomGate("default_id", self)
            else:
                new = gate_types[gate["gate"]]("default_id")

            new.load(gate)
            self.gates[key] = new

        # Instantiate and load paths
        for key in data_map["paths"]:
            new_path = Path("default_id")
            new_path.load(data_map["paths"][key])
            self.paths[key] = new_path

        self.temp_data = None  # Clear buffer after successful load
        logger.debug(f"Loaded Chip {self}")

    def __str__(self) -> str:
        """Return a string representation of the chip.

        Returns:
        - str: Formatted string with ID and counts.
        """
        return f"Chip (#{self.id}) {len(self.gates)} Gates / {len(self.paths)} Paths"

    def get_inputs(self) -> List[str]:
        """Retrieve the IDs of all gates defined as 'Input'.

        Returns:
        - List[str]: A list of gate IDs.
        """
        result: List[str] = []
        for i in self.gates:
            if self.gates[i].type == "Input":
                result.append(i)
        return result

    def get_outputs(self) -> List[str]:
        """Retrieve the IDs of all gates defined as 'Output'.

        Returns:
        - List[str]: A list of gate IDs.
        """
        result: List[str] = []
        for i in self.gates:
            if self.gates[i].type == "Output":
                result.append(i)
        return result

    def get_gates(self) -> List[str]:
        """Retrieve the IDs of all standard 'Gate' types.

        Returns:
        - List[str]: A list of gate IDs.
        """
        result: List[str] = []
        for i in self.gates:
            if self.gates[i].type == "Gate":
                result.append(i)
        return result
