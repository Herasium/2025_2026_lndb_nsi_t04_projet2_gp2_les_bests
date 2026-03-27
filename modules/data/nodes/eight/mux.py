from typing import Any, List

from modules.data.complex import Complex

"""Fournit la logique pour le composant de porte Mux 8 bits."""


class Mux(Complex):
    """Représente un composant de porte Mux 8 bits pour le routage des données du système."""

    def __init__(self, id: Any) -> None:
        """Initialise l'instance de la porte Mux.

        Args:
            id: Identifiant unique utilisé pour le suivi des composants du système.
        """
        super().__init__(id)

        self.name: str = "MUX"
        self.gate_type: str = "8MUX"

        self.inputs: List[int] = [0,0,0,0,0,0,0,0,0]
        self.outputs: List[int] = [0]

        self.inputs_sizes: List[int] = [8,8,8,8,8,8,8,8,8]
        self.outputs_sizes: List[int] = [8]

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()