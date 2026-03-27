from typing import List, Any

from modules.data.gate import Gate

"""Définitions des portes logiques pour la simulation de circuits."""


class Nor(Gate):
    """Représente une porte logique NON-OU (NOR) avec deux entrées et une sortie."""

    def __init__(self, id: Any) -> None:
        """Initialise la porte NOR avec l'état et la configuration par défaut.

        Args:
            id: Identifiant unique pour l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "NOR"
        self.type: str = "Gate"
        self.gate_type: str = "NOR"

        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [1]

        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()