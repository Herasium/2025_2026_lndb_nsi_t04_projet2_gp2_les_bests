"""Fournit l'implémentation de la porte de retard (Delay) pour les simulations de circuits logiques."""

from typing import Any, List

from modules.data.gate import Gate


class Delay(Gate):
    """Porte de retard, maintient le signal pendant 1 cycle (tick)."""

    def __init__(self, id: Any) -> None:
        """Initialise une nouvelle instance de la porte Delay.

        Args:
            id: Identifiant unique pour l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "DLY"
        self.type: str = "Gate"
        self.gate_type: str = "DLY"

        self.inputs: List[int] = [0]
        self.outputs: List[int] = [0]

        self.old_output: int = 0

        self.inputs_sizes: List[int] = [1]
        self.outputs_sizes: List[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()