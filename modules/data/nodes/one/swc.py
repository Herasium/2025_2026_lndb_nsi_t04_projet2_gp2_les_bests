"""Fournit l'implémentation de la porte SWC pour les simulations de circuits logiques."""

from typing import Any, List

from modules.data.gate import Gate


class Swc(Gate):
    """Porte Swc, offrant un moyen de désactiver la sortie d'une porte, empêchant sa propagation ultérieure."""

    def __init__(self, id: Any) -> None:
        """Initialise une nouvelle instance de la porte Swc.

        Args:
            id: Identifiant unique pour l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "SWC"
        self.type: str = "Gate"
        self.gate_type: str = "SWC"

        # Initialisation des entrées et des sorties
        self.inputs: List[int] = [0, 0]
        self.outputs: List[Any] = [None]

        # Définition des dimensions des entrées et sorties
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        # Calcul de l'affichage et génération du motif de tuile
        self.calculate_display()
        self.gen_tile_pattern()