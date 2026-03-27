from typing import Any, List

from modules.data.complex import Complex

"""Fournit la logique pour le composant registre 8 bits."""


class Register(Complex):
    """Représente un composant de registre 8 bits pour le routage des données du système."""

    def __init__(self, id: Any) -> None:
        """Initialise l'instance du registre.

        Args:
            id: Identifiant unique utilisé pour le suivi des composants du système.
        """
        super().__init__(id)

        self.name: str = "REGI"
        self.gate_type: str = "8REGISTER"

        self.inputs: List[int] = [0,0,0]
        self.outputs: List[int] = [0]

        self.inputs_sizes: List[int] = [8,1,1]
        self.outputs_sizes: List[int] = [8]

        self.current_value = 0

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()