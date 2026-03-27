from typing import List

from modules.data.gate import Gate


class Or(Gate):
    """Représente un composant de porte logique OU au sein de la simulation."""

    def __init__(self, id: str) -> None:
        """Initialise l'instance de la porte OU.

        Args:
            id: Un identifiant unique pour l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "OR"
        self.type: str = "Gate"
        self.gate_type: str = "OR"

        # Initialisation des entrées et sorties
        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0]

        # Tailles respectives des entrées et sorties
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        # Calcul de l'affichage et génération du motif de tuiles
        self.calculate_display()
        self.gen_tile_pattern()