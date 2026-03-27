"""Fournit des composants de portes logiques spécialisés pour les environnements de simulation."""

import math
from typing import List, Any
import random

from modules.data.complex import Complex


class Input(Complex):
    """Représente une porte d'entrée 8 bits au sein d'un circuit de simulation logique."""

    def __init__(self, id: Any) -> None:
        """Initialise le composant d'entrée.

        Args:
            id: Identifiant unique pour l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "IN"
        self.type: str = "Input"
        self.gate_type: str = "8Input"

        self.inputs: List[Any] = []
        self.outputs: List[int] = [1]
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = [8]

        # Décalage de taille exceptionnel
        self.exceptional_size_offset: int = 2

        self.gen_tile_pattern()
        self.calculate_display()
        self.setup_texts()

    def switch(self) -> None:
        """Simule un changement d'état d'entrée en générant un nouvel entier 8 bits aléatoire."""
        self.outputs[0] = random.randint(0, 255)
        self.gen_tile_pattern()
        self.update_text_readings()