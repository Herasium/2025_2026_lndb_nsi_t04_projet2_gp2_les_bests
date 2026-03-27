import math
from typing import List, Union

from modules.data.gate import Gate

"""Mise en œuvre d'une porte d'horloge pour la simulation de circuits."""


class Clock(Gate):
    """Représente un générateur de signal d'horloge au sein de l'environnement de simulation."""

    def __init__(self, id: Union[int, str]) -> None:
        """Initialise le composant Clock (Horloge).

        Args:
            id: Identifiant unique pour l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "CLK"
        self.type: str = "Gate"
        self.gate_type: str = "CLK"

        # Décalage de taille exceptionnel
        self.exceptional_size_offset: int = 2

        self.inputs: List[int] = []
        self.outputs: List[int] = [0]
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = [1]

        # Calcul de l'affichage et génération du motif de tuile
        self.calculate_display()
        self.gen_tile_pattern()