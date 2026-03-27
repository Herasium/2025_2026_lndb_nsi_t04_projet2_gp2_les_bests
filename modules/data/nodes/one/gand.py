"""Fournit les implémentations pour les composants de portes logiques standard."""

from typing import List, Union

from modules.data.gate import Gate


class And(Gate):
    """Représente une porte logique ET standard à deux entrées."""

    def __init__(self, id: Union[int, str]) -> None:
        """Initialise la porte ET avec les états d'entrée/sortie binaires par défaut.

        Args:
            id: Identifiant unique utilisé pour le suivi de l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "AND"
        self.type: str = "Gate"
        self.gate_type: str = "AND"

        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0]
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()