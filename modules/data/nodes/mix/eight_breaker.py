from typing import Any, List

from modules.data.complex import Complex

"""Fournit la logique pour le composant de porte d'interruption (breaker gate) 8 bits."""


class Breaker(Complex):
    """Représente un composant de porte d'interruption 8 bits pour l'aiguillage des données système."""

    def __init__(self, id: Any) -> None:
        """Initialise l'instance de la porte Breaker.

        Args:
            id: Identifiant unique utilisé pour le suivi des composants du système.
        """
        super().__init__(id)

        self.name: str = "BREAKER"
        self.gate_type: str = "8BREAK"

        # Initialisation des entrées et sorties
        self.inputs: List[int] = [0]
        self.outputs: List[int] = [0, 0, 0, 0, 0, 0, 0, 0]

        # Définition des tailles de bits pour les entrées et sorties
        self.inputs_sizes: List[int] = [8]
        self.outputs_sizes: List[int] = [1, 1, 1, 1, 1, 1, 1, 1]

        # Calcul de l'affichage, génération du motif de tuile et configuration des textes
        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()