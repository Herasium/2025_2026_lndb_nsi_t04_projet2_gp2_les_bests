import math
from typing import List, Any

from modules.data.gate import Gate

"""Fournit l'implémentation de la porte de sortie (Output) pour la simulation de circuit logique."""


class Output(Gate):
    """Représente un nœud de sortie dans le circuit.

    Attributs :
        name : Nom de l'identifiant interne de la porte.
        type : Classification générale de la porte.
        gate_type : Type opérationnel spécifique.
        inputs : Liste des états d'entrée booléens actuels.
        outputs : Liste des terminaux de sortie connectés.
        inputs_sizes : Dimensions requises pour les ports d'entrée.
        outputs_sizes : Dimensions requises pour les ports de sortie.
        exceptional_size_offset : Décalage vertical pour la logique de rendu.
        gate_width : Envergure horizontale de la représentation de la porte.
        gate_tile_pattern : Carte de grille aplatie pour le rendu graphique.
    """

    def __init__(self, id: Any) -> None:
        """Initialise l'instance de la porte de sortie (Output).

        Args :
            id : Identifiant unique pour l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "OUT"
        self.type: str = "Output"
        self.gate_type: str = "Output"

        # Initialisation des entrées et sorties
        self.inputs: List[int] = [0]
        self.outputs: List[Any] = []
        self.inputs_sizes: List[int] = [1]
        self.outputs_sizes: List[int] = []

        # Décalage spécifique pour l'affichage
        self.exceptional_size_offset: int = 2

        # Génération du modèle de tuiles et calcul de l'affichage
        self.gen_tile_pattern()
        self.calculate_display()