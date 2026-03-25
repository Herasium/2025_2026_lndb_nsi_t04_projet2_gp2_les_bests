import json
import os
from typing import Dict, List, Any, Union, Optional
from line_profiler import profile

from modules.data import data
from modules.data.gate_index import gate_types
from modules.data.nodes.path import Path
from modules.logger import Logger
from modules.ui.toolbox.id_generator import random_id
from modules.data.custom import CustomGate

logger: Logger = Logger("Chip")


class Chip:
    """Manages the lifecycle, serialization, and structure of a logic chip."""

    def __init__(self, id: str) -> None:
        """Initializes a new Chip instance.

        Args:
            id: Unique identifier for the chip.
        """
        self.paths: Dict[str, Path] = {}
        self.gates: Dict[str, Any] = {}
        self.id: str = id
        self.name: str = "Default Chip"
        self.type: str = "Chip"
        self.changed: bool = False
        self.requirements: List[str] = []
        self.temp_data: Optional[Dict] = None
        self.private = False

    @profile
    def copy(self) -> "Chip":
        """Creates a deep copy of the chip with a newly generated identifier.

        Returns:
            A new Chip instance reflecting the current state.
        """
        new: Chip = Chip("no_id")
        new.partial_load(json.loads(self.save(no_file=True, dojson=True)))
        new.load()
        new.id = random_id()
        return new

    @profile
    def save(
        self, no_file: bool = False, dojson: bool = False
    ) -> Union[Dict, str, None]:
        """Serializes chip state to a dictionary, JSON string, or disk.

        Args:
            no_file: Prevents disk I/O when true.
            dojson: Returns serialized output as a JSON string when true.

        Returns:
            The serialized representation or None if the chip was written to disk.
        """
        paths: Dict[str, Any] = {}
        gates: Dict[str, Any] = {}

        self.requirements = []

        for id in self.paths:
            paths[id] = self.paths[id].save()

        for id in self.gates:
            gates[id] = self.gates[id].save()
            if self.gates[id].type == "Custom":
                self.requirements.append(self.gates[id].base_chip_id)
                self.requirements += data.loaded_chips[
                    self.gates[id].base_chip_id
                ].requirements

        self.requirements = list(set(self.requirements))

        result: Dict[str, Any] = {
            "type": self.type,
            "name": self.name,
            "id": self.id,
            "gates": gates,
            "paths": paths,
            "version": data.VERSION,
            "requirements": self.requirements,
        }

        if no_file and not dojson:
            return result

        dump: str = json.dumps(result, indent=1)
        if dojson:
            return dump

        path: str = data.current_path
        os.makedirs(os.path.join(path, "saves"), exist_ok=True)
        file_path: str = os.path.join(os.path.join(path, "saves"), f"{self.id}.chip")

        with open(file_path, "wb") as file:
            file.write(dump.encode())

        logger.print(f"Saved {self.name}, #{self.id}")
        return None

    @profile
    def partial_load(self, data: Dict[str, Any]) -> None:
        """Loads core metadata and buffers structural data for final initialization.

        Args:
            data: Raw state dictionary.
        """
        self.type = data["type"]
        self.name = data["name"]
        self.id = data["id"]

        if data["version"] != "a.136":
            self.requirements = data["requirements"]

        self.temp_data = data

    @profile
    def load(self) -> None:
        """Constructs gates and paths from buffered data.

        Requires partial_load to be executed first.
        """
        if self.temp_data is None:
            logger.error("You must partial load a chip, before finishing load.")
            return

        data_map: Dict[str, Any] = self.temp_data

        for key in data_map["gates"]:
            gate = data_map["gates"][key]
            if gate["type"] in ["Gate", "Complex"]:
                new = gate_types[gate["gate"]]("default_id")
            elif gate["type"] == "Custom":
                new = CustomGate("default_id", Chip("default_chip"))
            else:
                new = gate_types[gate["gate"]]("default_id")

            new.load(gate)
            self.gates[key] = new

        for key in data_map["paths"]:
            new_path = Path("default_id")
            new_path.load(data_map["paths"][key])
            self.paths[key] = new_path

        self.temp_data = None
        logger.debug(f"Loaded Chip {self}")

    def __str__(self) -> str:
        """Provides a human-readable summary of the chip instance.

        Returns:
            A formatted string containing ID and object counts.
        """
        return f"Chip (#{self.id}) {len(self.gates)} Gates / {len(self.paths)} Paths"

    def get_inputs(self) -> List[str]:
        """Retrieves identifiers for all input-type gates.

        Returns:
            List of gate IDs.
        """
        result: List[str] = []
        for i in self.gates:
            if self.gates[i].gate_type in ["Input", "8Input"]:
                result.append(i)
        return result

    def get_outputs(self) -> List[str]:
        """Retrieves identifiers for all output-type gates.

        Returns:
            List of gate IDs.
        """
        result: List[str] = []
        for i in self.gates:
            if self.gates[i].type == "Output":
                result.append(i)
        return result

    def get_gates(self) -> List[str]:
        """Retrieves identifiers for all standard gate-type components.

        Returns:
            List of gate IDs.
        """
        result: List[str] = []
        for i in self.gates:
            if self.gates[i].type == "Gate":
                result.append(i)
        return result
