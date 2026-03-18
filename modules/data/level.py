import json
import os
import time
from typing import List, Dict, Any, Optional, Union
import random

from modules.data.chip import Chip
from modules.ui.toolbox.id_generator import random_id
from modules.data import data
from modules.logger import Logger
from modules.engine import Engine

logger: Logger = Logger("Level")


class Level:
    """Manages game level logic, including chip state, objectives, and progression.

    Attributes:
        chip (Chip): The logical chip associated with this level.
        engine (Engine): The simulation engine used to evaluate circuit logic.
    """

    def __init__(self, id: Union[int, str]) -> None:
        """Initializes the Level instance.

        Args:
            id: The identifier used to configure the base chip.
        """
        self.chip: Chip = Chip(id)
        self.number: int = 0
        self.time: int = 300
        self.id: str = f"level_{id}"
        self.name: str = "Default Level"
        self.description: str = "Basic level to learn the basis of gates."

        self.start_text: List[str] = []
        self.hints: List[str] = []
        self.truth: Dict[str, Any] = {}
        self.start: int = 1
        self.play: bool = False
        self.answer: Optional[Chip] = None

        self.max_usage: Dict[str, int] = {}
        self.inventory: Dict[str, int] = {}
        self.won: bool = False
        self.start_time: float = 0.0
        self.stars: int = 0
        self.shown_hints: bool = False
        self.shown_solution: bool = False
        self.color: int = 0
        self.category: int = 0
        self.is_custom: bool = False
        self.is_complex: bool = False
        self.truth_test_values: List[List[int]] = []
        self.engine: Engine = Engine()

    def play_mode(self) -> None:
        """Prepares the level for gameplay by resetting state and defining target logic."""
        if self.play:
            self.play = True
            self.chip = self.answer.copy()
            self.chip.id = random_id()
        else:
            self.play = True
            self.answer = self.chip
            self.chip = self.answer.copy()
            self.chip.id = random_id()

        self.won = False
        self.start_time = time.time()
        self.stars = 3
        self.shown_hints = False
        self.shown_solution = False
        self.chip.paths = {}
        self.is_complex = False

        left: List[str] = self.get_gates(self.chip)

        keys_to_delete: List[str] = [i for i in self.chip.gates.keys() if i in left]
        for key in keys_to_delete:
            del self.chip.gates[key]

        self.calculate_inventory()
        self.setup_random_test_values()
        self.get_truth_table(answer=True)

    def setup_random_test_values(self):
        
        inputs: List[str] = self.get_inputs(self.answer)
        self.truth_test_values = []

        for _ in range(10):
            values = []
            for i in inputs:
                values.append(random.randint(0,2**self.answer.gates[i].outputs_sizes[0]-1))
            self.truth_test_values.append(values)



    def get_stars_count(self) -> int:
        """Calculates current star rating based on time and hint usage.

        Returns:
            The number of stars earned, ranging from 0 to 3.
        """
        self.stars = 3

        if round(time.time() - self.start_time) > self.time:
            self.stars -= 1

        if self.shown_hints or self.shown_solution:
            self.stars -= 1

        return self.stars

    def calculate_inventory(self) -> None:
        """Computes gate usage requirements and current player usage."""
        self.max_usage = {}
        for i in self.answer.gates:
            if self.answer.gates[i].type == "Custom":
                key = self.answer.gates[i].base_chip_id
                self.max_usage[key] = self.max_usage.get(key, 0) + 1
            else:
                key = self.answer.gates[i].gate_type
                self.max_usage[key] = self.max_usage.get(key, 0) + 1
            
            if self.answer.gates[i].type == "Complex":
                self.is_complex = True

        self.inventory = {}
        for i in self.chip.gates:
            if self.chip.gates[i].type == "Custom":
                key = self.chip.gates[i].base_chip_id
                self.inventory[key] = self.inventory.get(key, 0) + 1
            else:
                key = self.chip.gates[i].gate_type
                self.inventory[key] = self.inventory.get(key, 0) + 1

    def start_chip(self, chip: Optional[Chip] = None) -> None:
        """Resets gate I/O states within the specified chip.

        Args:
            chip: The chip to initialize; defaults to current chip if None.
        """
        if chip is None:
            chip = self.chip

        if self.start == 1:
            for i in chip.gates:
                chip.gates[i].inputs = [False for _ in chip.gates[i].inputs]
                chip.gates[i].outputs = [False for _ in chip.gates[i].outputs]
        elif self.start == 2:
            for i in chip.gates:
                chip.gates[i].inputs = [True for _ in chip.gates[i].inputs]
                chip.gates[i].outputs = [True for _ in chip.gates[i].outputs]

    def get_inputs(self, chip: Optional[Chip] = None) -> List[str]:
        """Identifies all input gate IDs.

        Args:
            chip: The chip to inspect.

        Returns:
            A list of gate IDs acting as inputs.
        """
        if chip is None:
            chip = self.chip
        return [i for i in self.chip.gates if self.chip.gates[i].type == "Input"]

    def get_outputs(self, chip: Optional[Chip] = None) -> List[str]:
        """Identifies all output gate IDs.

        Args:
            chip: The chip to inspect.

        Returns:
            A list of gate IDs acting as outputs.
        """
        if chip is None:
            chip = self.chip
        return [i for i in self.chip.gates if self.chip.gates[i].type == "Output"]

    def get_gates(self, chip: Optional[Chip] = None) -> List[str]:
        """Identifies all functional logic gate IDs.

        Args:
            chip: The chip to inspect.

        Returns:
            A list of gate IDs for standard or custom gates.
        """
        if chip is None:
            chip = self.chip
        return [
            i for i in self.chip.gates if self.chip.gates[i].type in ["Gate", "Custom","Complex"]
        ]

    def compare_truth_tables(self) -> bool:
        """Validates the current chip against the expected solution truth table.

        Returns:
            True if the truth tables match, False otherwise.
        """
        if self.answer is None:
            return False
        if self.answer.id not in self.truth or self.chip.id not in self.truth:
            return False

        for i in self.truth[self.answer.id]["data"]:
            if (
                self.truth[self.answer.id]["data"][i]
                != self.truth[self.chip.id]["data"][i]
            ):
                return False
        return True

    def check_victory(self) -> bool:
        """Determines if the level objectives have been met.

        Returns:
            Current victory state.
        """
        self.won = self.compare_truth_tables()
        return self.won

    def get_single_truth_table_complex(self, chip: Chip) -> None:
        """Generates a truth table for the provided simple chip.

        Args:
            chip: The instance to evaluate.
        """
        copy: Chip = chip.copy()
        self.start_chip(copy)
        self.engine.propagate_values(copy)

        inputs: List[str] = self.get_inputs(copy)
        outputs: List[str] = self.get_outputs(copy)
        size: int = len(inputs)

        self.truth[chip.id]["meta"].update(
            {"size": size, "inputs": inputs, "outputs": outputs,"values":self.truth_test_values,"complex": True}
        )
        count = 0
        for current in self.truth_test_values:
            for index in range(len(inputs)):
                copy.gates[inputs[index]].outputs[0] = current[index]

            self.engine.propagate_values(copy)

            result = [copy.gates[i].inputs[0] for i in outputs]
            self.truth[chip.id]["data"][count] = result
            count += 1

    def get_single_truth_table_simple(self,chip: Chip) -> None:
        """Generates a truth table for the provided complex chip.

        Args:
            chip: The instance to evaluate.
        """
        copy: Chip = chip.copy()
        self.start_chip(copy)
        self.engine.propagate_values(copy)

        inputs: List[str] = self.get_inputs(copy)
        outputs: List[str] = self.get_outputs(copy)
        size: int = len(inputs)

        self.truth[chip.id]["meta"].update(
            {"size": size, "inputs": inputs, "outputs": outputs, "power": 2**size,"complex": False}
        )

        power: int = 2**size
        for current in range(power):
            # Generate binary state combinations for truth table rows
            values = [bool(current & (1 << i)) for i in range(size)]
            for index in range(len(inputs)):
                copy.gates[inputs[index]].outputs[0] = values[index]

            self.engine.propagate_values(copy)

            result = [copy.gates[i].inputs[0] for i in outputs]
            # Map bit array to integer index for the results dictionary
            int_value = sum(b << i for i, b in enumerate(reversed(values)))
            self.truth[chip.id]["data"][int_value] = result

    def get_truth_table(self, answer: bool = False) -> None:
        """Initializes truth table storage and triggers generation.

        Args:
            answer: If True, evaluates the solution chip; otherwise, the player chip.
        """
        used: Chip = self.answer if answer else self.chip
        self.truth[used.id] = {"meta": {}, "data": {}}
        if self.is_complex:
            self.get_single_truth_table_complex(used)
        else:
            self.get_single_truth_table_simple(used)

    def save(self) -> None:
        """Serializes current level and chip configuration to a file."""
        chip_save = self.chip.save(no_file=True)
        requirements: List[Dict[str, Any]] = []
        for i in chip_save["requirements"]:
            requirements.append(data.loaded_chips[i].save(no_file=True))

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
                "is_custom": self.is_custom,
            },
        }

        dump: str = json.dumps(result, indent=1)
        path: str = data.current_path
        save_dir: str = os.path.join(path, "levels")
        os.makedirs(save_dir, exist_ok=True)

        file_path: str = os.path.join(save_dir, f"{self.id}.level")
        with open(file_path, "wb") as file:
            file.write(dump.encode())

        logger.success(f"Saved level {self.id}")

    def load(self, data: Dict[str, Any]) -> None:
        """Hydrates the level state from a configuration dictionary.

        Args:
            data: The source dictionary containing level parameters.
        """
        self.chip.partial_load(data["chip"])
        self.chip.load()

        self.time = data["level"]["time"]
        self.id = data["level"]["id"]
        self.number = data["level"]["number"]
        self.description = data["level"]["description"]
        self.hints = data["level"]["hints"]
        self.name = data["level"]["name"]
        self.start = data["level"]["start"]
        self.color = data["level"]["color"]
        self.category = data["level"]["category"]

        if data["level"]["version"] > 200:
            self.is_custom = data["level"]["is_custom"]

        logger.debug(f"Loaded Level {self}")

    def __str__(self) -> str:
        """Provides a string representation of the level.

        Returns:
            The level ID, name, and index.
        """
        return f"Level (#{self.id}) {self.name} {self.number}"
