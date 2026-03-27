from typing import Any, List

from modules.data.complex import Complex

"""Fournit la logique pour le composant de porte de rupture (breaker gate) 8-bit."""


class Breaker(Complex):
    """Représente un composant de porte de rupture 8-bit pour l'acheminement des données système."""

    def __init__(self, id: Any) -> None:
        """Initialise l'instance de la porte Breaker.

        Args:
            id: Identifiant unique utilisé pour le suivi des composants du système.
        """
        super().__init__(id)

        self.name: str = "BREAKER"
        self.gate_type: str = "8BREAK"

        # Entrées et sorties initiales
        self.inputs: List[int] = [0]
        self.outputs: List[int] = [0, 0, 0, 0, 0, 0, 0, 0]

        # Tailles respectives des ports d'entrée et de sortie
        self.inputs_sizes: List[int] = [8]
        self.outputs_sizes: List[int] = [1, 1, 1, 1, 1, 1, 1, 1]

        # Initialisation de l'affichage, du motif de tuile et des textes
        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()