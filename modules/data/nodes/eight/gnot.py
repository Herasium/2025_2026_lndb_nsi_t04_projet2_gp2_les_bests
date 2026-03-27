from typing import Any

from modules.data.complex import Complex

"""Fournit des implémentations de portes logiques 8 bits pour la simulation de circuits."""


class Not(Complex):
    """Représente un composant de porte logique NON (NOT) 8 bits.

    Attributs :
        name : Le nom d'affichage de la porte.
        gate_type : L'identifiant de la catégorie de porte logique.
        inputs : Décalages de broches (offsets) pour les signaux d'entrée.
        outputs : Décalages de broches (offsets) pour les signaux de sortie.
        inputs_sizes : Largeur de bit des broches d'entrée.
        outputs_sizes : Largeur de bit des broches de sortie.
    """

    def __init__(self, id: Any) -> None:
        """Initialise l'instance de la porte NON.

        Args :
            id : Un identifiant unique pour le composant.
        """
        super().__init__(id)

        self.name: str = "NOT"
        self.gate_type: str = "8NOT"

        self.inputs: list[int] = [0]
        self.outputs: list[int] = [255]
        self.inputs_sizes: list[int] = [8]
        self.outputs_sizes: list[int] = [8]

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()