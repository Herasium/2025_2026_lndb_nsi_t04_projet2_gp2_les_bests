"""Fournit l'implémentation de la porte Pass pour les simulations de circuits logiques."""

from typing import Any, List

from modules.data.gate import Gate


class Pass(Gate):
    """Composant tampon (buffer) qui propage les signaux d'entrée sans modification."""

    def __init__(self, id: Any) -> None:
        """Initialise une nouvelle instance de la porte Pass.

        Args:
            id: Identifiant unique pour l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "PASS"
        self.type: str = "Gate"
        self.gate_type: str = "PASS"

        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0, 0]

        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1, 1]

        self.calculate_display()
        self.gen_tile_pattern()