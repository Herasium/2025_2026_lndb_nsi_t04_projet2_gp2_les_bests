from typing import Any

from modules.data.complex import Complex

"""Fournit des implémentations de portes logiques 8-bit pour la simulation de circuits."""


class Nand(Complex):
    """Représente un composant de porte logique Nand 8-bit.

    Attributs :
        name : Le nom d'affichage de la porte.
        gate_type : L'identifiant de la catégorie de la porte logique.
        inputs : Décalages des broches pour les signaux d'entrée.
        outputs : Décalages des broches pour les signaux de sortie.
        inputs_sizes : Largeur de bits des broches d'entrée.
        outputs_sizes : Largeur de bits des broches de sortie.
    """

    def __init__(self, id: Any) -> None:
        """Initialise l'instance de la porte Nand.

        Args :
            id : Un identifiant unique pour le composant.
        """
        super().__init__(id)

        self.name: str = "NAND"
        self.gate_type: str = "8NAND"

        self.inputs: list[int] = [0, 0]
        self.outputs: list[int] = [0]
        self.inputs_sizes: list[int] = [8, 8]
        self.outputs_sizes: list[int] = [8]

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()