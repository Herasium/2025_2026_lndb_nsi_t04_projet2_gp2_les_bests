from typing import Any

from modules.data.gate import Gate

"""Mise en œuvre de la logique de porte pour l'état ON."""


class On(Gate):
    """Représente une porte logique de type ON."""

    def __init__(self, id: Any) -> None:
        """Initialise l'instance de la porte avec les métadonnées et les configurations de ports requises.

        Args:
            id: Identifiant unique attribué à cette instance de porte.
        """
        super().__init__(id)

        self.name: str = "ON"
        self.type: str = "Input"
        self.gate_type: str = "ON"

        self.inputs: list[int] = []
        self.outputs: list[int] = [1]

        self.inputs_sizes: list[int] = []
        self.outputs_sizes: list[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()

    def switch(self):
        # Méthode permettant de basculer l'état de la porte
        pass