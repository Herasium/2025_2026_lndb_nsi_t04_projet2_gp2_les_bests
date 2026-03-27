import math
from typing import List, Any

from modules.data.complex import Complex

"""Fournit la classe Output pour le rendu des composants de porte de sortie au sein de l'interface utilisateur."""


class Output(Complex):
    """Représente un composant de porte de sortie dans le système d'interface utilisateur."""

    def __init__(self, id: Any) -> None:
        """Initialise le composant de porte Output.

        Args:
            id: L'identifiant unique pour l'instance du composant.
        """
        super().__init__(id)

        self.name: str = "OUT"
        self.type: str = "Output"
        self.gate_type: str = "8Output"

        self.inputs: List[int] = [0]
        self.outputs: List[Any] = []
        self.inputs_sizes: List[int] = [8]
        self.outputs_sizes: List[int] = []

        # Décalage de taille exceptionnel
        self.exceptional_size_offset: int = 2

        self.gen_tile_pattern() # Génération du motif de tuiles
        self.calculate_display() # Calcul de l'affichage
        self.setup_texts() # Configuration des textes