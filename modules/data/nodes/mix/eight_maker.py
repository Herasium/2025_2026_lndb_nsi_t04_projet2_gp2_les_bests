"""Fournit l'implémentation de la porte Maker pour l'agrégation de signaux 8 bits."""

from typing import List, Any
from modules.data.complex import Complex


class Maker(Complex):
    """Agrège huit entrées de signaux de 1 bit en une seule sortie de 8 bits."""

    def __init__(self, id: Any) -> None:
        """Initialise l'instance de la porte Maker.

        Args:
            id: Identifiant unique pour l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "MAKER"
        self.gate_type: str = "8MAKER"

        # Initialisation des entrées (8 signaux de 1 bit)
        self.inputs: List[int] = [0, 0, 0, 0, 0, 0, 0, 0]
        # Initialisation de la sortie (1 signal de 8 bits)
        self.outputs: List[int] = [0]

        self.inputs_sizes: List[int] = [1, 1, 1, 1, 1, 1, 1, 1]
        self.outputs_sizes: List[int] = [8]

        # Calcul de l'affichage, génération du motif de tuile et configuration des textes
        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()