from typing import Any

from modules.data.complex import Complex

"""Fournit des implémentations de portes logiques 8 bits pour la simulation de circuits."""


class ONE(Complex):
    """Représente une valeur logique 1.

    Attributs :
        name : Le nom d'affichage de la porte.
        gate_type : L'identifiant de la catégorie de porte logique.
        inputs : Décalages de broches pour les signaux d'entrée.
        outputs : Décalages de broches pour les signaux de sortie.
        inputs_sizes : Largeur de bits des broches d'entrée.
        outputs_sizes : Largeur de bits des broches de sortie.
    """

    def __init__(self, id: Any) -> None:
        """Initialise l'instance de la porte NON.

        Args :
            id : Un identifiant unique pour le composant.
        """
        super().__init__(id)

        self.name: str = "ONE"
        self.type: str = "Input"
        self.gate_type: str = "8ONE"

        self.inputs: list[int] = []
        self.outputs: list[int] = [1]
        self.inputs_sizes: list[int] = []
        self.outputs_sizes: list[int] = [8]

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()

    def switch(self):
        # Méthode pour basculer l'état
        pass