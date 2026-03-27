"""Fournit les implémentations pour les composants de portes logiques standard."""

from typing import List, Union

from modules.data.gate import Gate


class Adder(Gate):
    """Représente une porte additionneur complet (Full Adder) standard."""

    def __init__(self, id: Union[int, str]) -> None:
        """Initialise la porte Adder avec des états d'entrée/sortie binaires par défaut.

        Args:
            id: Identifiant unique utilisé pour le suivi de l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "ADDER"
        self.type: str = "Gate"
        self.gate_type: str = "ADDER"

        self.inputs: List[int] = [0, 0, 0]
        self.outputs: List[int] = [0, 0]
        self.inputs_sizes: List[int] = [1, 1, 1]
        self.outputs_sizes: List[int] = [1, 1]

        self.calculate_display()
        self.gen_tile_pattern()