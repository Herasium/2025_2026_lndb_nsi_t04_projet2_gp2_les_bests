from typing import Any, List

from modules.data.complex import Complex

"""Fournit la logique pour le composant registre 8 bits."""


class Register(Complex):
    """Représente un composant de registre 8 bits pour l'acheminement des données système."""

    def __init__(self, id: Any) -> None:
        """Initialise l'instance du registre.

        Args:
            id: Identifiant unique utilisé pour le suivi des composants du système.
        """
        super().__init__(id)

        self.name: str = "REGI"
        self.gate_type: str = "8REGISTER"

        # Initialisation des entrées et sorties
        self.inputs: List[int] = [0, 0, 0]
        self.outputs: List[int] = [0]

        # Tailles des bus de données pour les entrées et sorties
        self.inputs_sizes: List[int] = [8, 1, 1]
        self.outputs_sizes: List[int] = [8]

        self.current_value = 0

        # Configuration de l'affichage et de l'interface graphique
        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()