"""Fournit des implémentations de portes logiques 8 bits pour la simulation de circuits."""

from typing import List, Union
from modules.data.complex import Complex


class Sub(Complex):
    """Représente un composant de porte logique de soustraction complète (Full Sub) 8 bits.

    Attributs :
        name : Le nom d'affichage de la porte.
        gate_type : L'identifiant de la catégorie de porte logique.
        inputs : Décalages des broches pour les signaux d'entrée.
        outputs : Décalages des broches pour les signaux de sortie.
        inputs_sizes : Largeur de bits des broches d'entrée.
        outputs_sizes : Largeur de bits des broches de sortie.
    """

    def __init__(self, id: Union[int, str]) -> None:
        """Initialise la porte Sub avec les états d'entrée/sortie binaires par défaut.

        Args :
            id : Identifiant unique utilisé pour le suivi de l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "SUB"
        self.gate_type: str = "8SUB"

        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0]
        self.inputs_sizes: List[int] = [8, 8]
        self.outputs_sizes: List[int] = [8]

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()