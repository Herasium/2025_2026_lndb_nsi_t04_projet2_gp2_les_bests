from typing import Any

from modules.data.gate import Gate

"""Implémentation de la porte logique pour l'opération NON (NOT)."""


class Not(Gate):
    """Représente une porte logique NON."""

    def __init__(self, id: Any) -> None:
        """Initialise l'instance de la porte avec les métadonnées requises et les configurations de ports.

        Args:
            id: Identifiant unique attribué à cette instance de porte.
        """
        super().__init__(id)

        self.name: str = "NOT"
        self.type: str = "Gate"
        self.gate_type: str = "NOT"

        self.inputs: list[int] = [0]
        self.outputs: list[int] = [1]

        self.inputs_sizes: list[int] = [1]
        self.outputs_sizes: list[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()