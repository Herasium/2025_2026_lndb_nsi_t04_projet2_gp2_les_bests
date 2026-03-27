"""Fournit des implémentations pour les composants de portes logiques standards."""

from typing import List, Union

from modules.data.gate import Gate


class Sub(Gate):
    """Représente une porte logique standard de type Soustracteur Complet (Full Sub)."""

    def __init__(self, id: Union[int, str]) -> None:
        """Initialise la porte Sub avec des états d'entrée/sortie binaires par défaut.

        Args:
            id: Identifiant unique utilisé pour le suivi de l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "SUB"
        self.type: str = "Gate"
        self.gate_type: str = "SUB"

        self.inputs: List[int] = [0, 0, 0]
        self.outputs: List[int] = [0, 0]
        self.inputs_sizes: List[int] = [1, 1, 1]
        self.outputs_sizes: List[int] = [1, 1]

        self.calculate_display()
        self.gen_tile_pattern()