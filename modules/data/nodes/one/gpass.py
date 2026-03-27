"""Fournit l'implémentation de la porte Pass pour les simulations de circuits logiques."""

from typing import Any, List

from modules.data.gate import Gate


class Pass(Gate):
    """Composant tampon qui propage les signaux d'entrée sans modification."""

    def __init__(self, id: Any) -> None:
        """Initialise une nouvelle instance de la porte Pass.

        Args:
            id: Identifiant unique pour l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "PASS"
        self.type: str = "Gate"
        self.gate_type: str = "PASS"

        # Initialisation des entrées et sorties
        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0, 0]

        # Définition de la taille des entrées et sorties
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1, 1]

        # Calcul de l'affichage et génération du motif de tuile
        self.calculate_display()
        self.gen_tile_pattern()