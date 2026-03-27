"""Fournit des implémentations pour les composants standards de portes logiques."""

from typing import List, Union

from modules.data.gate import Gate


class And(Gate):
    """Représente une porte logique ET standard à deux entrées."""

    def __init__(self, id: Union[int, str]) -> None:
        """Initialise la porte ET avec les états binaires d'entrée/sortie par défaut.

        Args:
            id: Identifiant unique utilisé pour le suivi de l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "AND"
        self.type: str = "Gate"
        self.gate_type: str = "AND"

        # Initialisation des états d'entrée et de sortie
        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0]
        
        # Définition des dimensions des entrées et sorties
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        # Calcul de l'affichage et génération du motif de tuiles
        self.calculate_display()
        self.gen_tile_pattern()