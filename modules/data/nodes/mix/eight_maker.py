"""Fournit l'implémentation de la porte Maker pour l'agrégation de signaux 8 bits."""

from typing import List, Any
from modules.data.complex import Complex


class Maker(Complex):
    """Agrège huit entrées de signaux 1 bit en une seule sortie de 8 bits."""

    def __init__(self, id: Any) -> None:
        """Initialise l'instance de la porte Maker.

        Args:
            id: Identifiant unique pour l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "MAKER"
        self.gate_type: str = "8MAKER"

        self.inputs: List[int] = [0, 0, 0, 0, 0, 0, 0, 0]
        self.outputs: List[int] = [0]

        self.inputs_sizes: List[int] = [1, 1, 1, 1, 1, 1, 1, 1]
        self.outputs_sizes: List[int] = [8]

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()