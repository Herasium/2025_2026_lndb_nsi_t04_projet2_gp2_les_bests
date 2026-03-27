import math
from typing import List, Any

from modules.data.gate import Gate

"""Fournit l'implémentation de la porte d'entrée (Input) pour la simulation de circuit."""


class Input(Gate):
    """Représente une porte d'entrée à bascule manuelle au sein d'un circuit."""

    def __init__(self, id: Any) -> None:
        """Initialise la porte d'entrée (Input).

        Args:
            id: Identifiant unique pour l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "IN"
        self.type: str = "Input"
        self.gate_type: str = "Input"

        self.inputs: List[Any] = []
        self.outputs: List[int] = [1]
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = [1]

        self.exceptional_size_offset: int = 2

        self.gen_tile_pattern()
        self.calculate_display()

    def switch(self) -> None:
        """Bascule l'état de sortie actuel entre 0 et 1."""
        # Convertit l'inversion booléenne en représentation entière
        self.outputs[0] = (not self.outputs[0] == 1) * 1
        self.gen_tile_pattern()