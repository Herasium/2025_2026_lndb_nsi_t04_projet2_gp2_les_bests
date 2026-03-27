from typing import Any, List

from modules.data.complex import Complex

"""Fournit la logique pour le composant porte Multiplexeur (Mux) 8-bit."""


class Mux(Complex):
    """Représente un composant porte Mux 8-bit pour le routage des données du système."""

    def __init__(self, id: Any) -> None:
        """Initialise l'instance de la porte Mux.

        Args:
            id: Identifiant unique utilisé pour le suivi des composants du système.
        """
        super().__init__(id)

        self.name: str = "MUX"
        self.gate_type: str = "8MUX"

        # Initialisation des entrées et sorties
        self.inputs: List[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.outputs: List[int] = [0]

        # Définition des tailles des entrées et sorties (8-bit)
        self.inputs_sizes: List[int] = [8, 8, 8, 8, 8, 8, 8, 8, 8]
        self.outputs_sizes: List[int] = [8]

        # Calcul de l'affichage, génération du motif de tuile et configuration des textes
        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()