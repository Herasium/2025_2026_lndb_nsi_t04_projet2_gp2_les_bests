import json
import os
import time
from typing import List, Dict, Any, Optional, Union

from modules.data.chip import Chip
from modules.ui.toolbox.id_generator import random_id
from modules.data import data
from modules.logger import Logger
from modules.engine import Engine

# Initialize the logger for the Level class
logger: Logger = Logger("Level")


class Level:
    """
    Represents a game level containing a logic chip, objectives, and state management.
    """

    def __init__(self, id: Union[int, str]) -> None:
        """Initialize a new Level instance.

        Parameters:
        - id: The unique identifier used to generate the level ID and chip.

        Returns:
        - None
        """
        # Core data structures
        self.chip: Chip = Chip(id)
        self.number: int = 0
        self.time: int = 300
        self.id: str = f"level_{id}"
        self.name: str = "Default Level"
        self.description: str = "Basic level to learn the basis of gates."

        # Level configuration and state
        self.start_text: List[str] = []
        self.hints: List[str] = []
        self.truth: Dict[str, Any] = {}
        self.start: int = 1
        self.play: bool = False
        self.answer: Optional[Chip] = None

        # Inventory and scoring tracking
        self.max_usage: Dict[str, int] = {}
        self.inventory: Dict[str, int] = {}
        self.won: bool = False
        self.start_time: float = 0.0
        self.stars: int = 0
        self.shown_hints: bool = False
        self.shown_solution: bool = False
        self.color: int = 0
        self.category: int = 0
        self.engine: Engine = Engine()

    def play_mode(self) -> None:
        """Switch the level into play mode, preparing the chip and truth tables.

        Returns:
        - None
        """
        # Determine if we are restarting or starting fresh
        if self.play:
            self.play = True
            self.chip = self.answer.copy()
            self.chip.id = random_id()
        else:
            self.play = True
            self.answer = self.chip
            self.chip = self.answer.copy()
            self.chip.id = random_id()

        # Reset game state for the attempt
        self.won = False
        self.start_time = time.time()
        self.stars = 3
        self.shown_hints = False
        self.shown_solution = False
        self.chip.paths = {}

        # Get gate IDs that need to be removed for the player to solve
        left: List[str] = self.get_gates(self.chip)

        # Clear existing gates from the player's chip
        keys_to_delete: List[str] = [i for i in self.chip.gates.keys() if i in left]
        for key in keys_to_delete:
            del self.chip.gates[key]

        # Refresh inventory counts and the solution truth table
        self.calculate_inventory()
        self.get_truth_table(answer=True)

    def get_stars_count(self) -> int:
        """Calculate and return the number of stars earned based on performance.

        Returns:
        - int: The star rating (0 to 3).
        """
        self.stars = 3

        # Penalize for exceeding the time limit
        if round(time.time() - self.start_time) > self.time:
            self.stars -= 1

        # Penalize for using help features
        if self.shown_hints or self.shown_solution:
            self.stars -= 1

        return self.stars

    def calculate_inventory(self) -> None:
        """Calculate the maximum allowed gates and current gate usage.

        Returns:
        - None
        """
        self.max_usage = {}
        # Count gates in the solution (answer) to set limits
        for i in self.answer.gates:
            if self.answer.gates[i].type == "Custom":
                key = self.answer.gates[i].base_chip_id
                self.max_usage[key] = self.max_usage.get(key, 0) + 1
            else:
                key = self.answer.gates[i].gate_type
                self.max_usage[key] = self.max_usage.get(key, 0) + 1

        self.inventory = {}
        # Count gates currently placed in the player's chip
        for i in self.chip.gates:
            if self.chip.gates[i].type == "Custom":
                key = self.chip.gates[i].base_chip_id
                self.inventory[key] = self.inventory.get(key, 0) + 1
            else:
                key = self.chip.gates[i].gate_type
                self.inventory[key] = self.inventory.get(key, 0) + 1

    def start_chip(self, chip: Optional[Chip] = None) -> None:
        """Initialize the input/output states of all gates in a chip.

        Parameters:
        - chip: The chip to initialize. Defaults to self.chip if None.

        Returns:
        - None
        """
        if chip is None:
            chip = self.chip

        # Set all pins to False if start mode is 1
        if self.start == 1:
            for i in chip.gates:
                chip.gates[i].inputs = [False for _ in chip.gates[i].inputs]
                chip.gates[i].outputs = [False for _ in chip.gates[i].outputs]
        # Set all pins to True if start mode is 2
        elif self.start == 2:
            for i in chip.gates:
                chip.gates[i].inputs = [True for _ in chip.gates[i].inputs]
                chip.gates[i].outputs = [True for _ in chip.gates[i].outputs]

    def get_inputs(self, chip: Optional[Chip] = None) -> List[str]:
        """Retrieve the IDs of all input-type gates in the chip.

        Parameters:
        - chip: The chip to inspect. Defaults to self.chip if None.

        Returns:
        - List[str]: List of gate IDs that are inputs.
        """
        if chip is None:
            chip = self.chip
        return [i for i in self.chip.gates if self.chip.gates[i].type == "Input"]

    def get_outputs(self, chip: Optional[Chip] = None) -> List[str]:
        """Retrieve the IDs of all output-type gates in the chip.

        Parameters:
        - chip: The chip to inspect. Defaults to self.chip if None.

        Returns:
        - List[str]: List of gate IDs that are outputs.
        """
        if chip is None:
            chip = self.chip
        return [i for i in self.chip.gates if self.chip.gates[i].type == "Output"]

    def get_gates(self, chip: Optional[Chip] = None) -> List[str]:
        """Retrieve the IDs of all standard or custom logic gates in the chip.

        Parameters:
        - chip: The chip to inspect. Defaults to self.chip if None.

        Returns:
        - List[str]: List of gate IDs that are functional logic gates.
        """
        if chip is None:
            chip = self.chip
        return [
            i for i in self.chip.gates if self.chip.gates[i].type in ["Gate", "Custom"]
        ]

    def compare_truth_tables(self) -> bool:
        """Compare the current chip's truth table against the answer's truth table.

        Returns:
        - bool: True if the tables match, False otherwise.
        """
        if self.answer is None:
            return False
        if self.answer.id not in self.truth or self.chip.id not in self.truth:
            return False

        # Check every entry in the data section of the truth tables
        for i in self.truth[self.answer.id]["data"]:
            if (
                self.truth[self.answer.id]["data"][i]
                != self.truth[self.chip.id]["data"][i]
            ):
                return False
        return True

    def check_victory(self) -> bool:
        """Update the won status by comparing truth tables.

        Returns:
        - bool: The current victory status.
        """
        self.won = self.compare_truth_tables()
        return self.won

    def get_single_truth_table(self, chip: Chip) -> None:
        """Generate and store the truth table for a specific chip.

        Parameters:
        - chip: The Chip instance to analyze.

        Returns:
        - None
        """
        # Work on a copy to avoid mutating the active game state
        copy: Chip = chip.copy()
        self.start_chip(copy)
        self.engine.propagate_values(copy)

        inputs: List[str] = self.get_inputs(copy)
        outputs: List[str] = self.get_outputs(copy)
        size: int = len(inputs)

        # Store metadata
        self.truth[chip.id]["meta"].update(
            {"size": size, "inputs": inputs, "outputs": outputs, "power": 2**size}
        )

        power: int = 2**size
        # Iterate through every possible input combination
        for current in range(power):
            # Convert integer to bit array for inputs
            values = [bool(current & (1 << i)) for i in range(size)]
            for index in range(len(inputs)):
                copy.gates[inputs[index]].outputs[0] = values[index]

            # Run simulation
            self.engine.propagate_values(copy)

            # Capture output state
            result = [copy.gates[i].inputs[0] for i in outputs]
            int_value = sum(b << i for i, b in enumerate(reversed(values)))
            self.truth[chip.id]["data"][int_value] = result

    def get_truth_table(self, answer: bool = False) -> None:
        """Wrapper to generate a truth table for either the current chip or the answer.

        Parameters:
        - answer: If True, generates the table for the solution; otherwise for the current chip.

        Returns:
        - None
        """
        used: Chip = self.answer if answer else self.chip
        self.truth[used.id] = {"meta": {}, "data": {}}
        self.get_single_truth_table(used)

    def save(self) -> None:
        """Serialize and save the level data to a .level file.

        Returns:
        - None
        """
        # Prepare chip and requirement data
        chip_save = self.chip.save(no_file=True)
        requirements: List[Dict[str, Any]] = []
        for i in chip_save["requirements"]:
            requirements.append(data.loaded_chips[i].save(no_file=True))

        # Compile level structure
        result: Dict[str, Any] = {
            "chip": chip_save,
            "requirements": requirements,
            "level": {
                "time": self.time,
                "id": self.id,
                "number": self.number,
                "name": self.name,
                "description": self.description,
                "hints": self.hints,
                "version": data.VERSION,
                "start": self.start,
                "truth": self.truth,
                "color": self.color,
                "category": self.category,
            },
        }

        # Handle file writing
        dump: str = json.dumps(result, indent=1)
        path: str = data.current_path
        save_dir: str = os.path.join(path, "levels")
        os.makedirs(save_dir, exist_ok=True)

        file_path: str = os.path.join(save_dir, f"{self.id}.level")
        with open(file_path, "wb") as file:
            file.write(dump.encode())

        logger.success(f"Saved level {self.id}")

    def load(self, data: Dict[str, Any]) -> None:
        """Load level and chip data from a dictionary.

        Parameters:
        - data: Dictionary containing level configuration and chip state.

        Returns:
        - None
        """
        # Restore chip state
        self.chip.partial_load(data["chip"])
        self.chip.load()

        # Restore level metadata
        self.time = data["level"]["time"]
        self.id = data["level"]["id"]
        self.number = data["level"]["number"]
        self.description = data["level"]["description"]
        self.hints = data["level"]["hints"]
        self.name = data["level"]["name"]
        self.start = data["level"]["start"]
        self.color = data["level"]["color"]
        self.category = data["level"]["category"]

        logger.debug(f"Loaded Level {self}")

    def __str__(self) -> str:
        """Provide a string representation of the Level.

        Returns:
        - str: Formatted level details.
        """
        return f"Level (#{self.id}) {self.name} {self.number}"
