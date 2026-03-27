from typing import List, Any

from modules.data.gate import Gate


class Xor(Gate):
    """Représente un composant de porte logique XOR."""

    def __init__(self, id: Any) -> None:
        """Initialise la porte XOR avec les configurations de broches par défaut.

        Args:
            id: L'identifiant unique pour l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "XOR"
        self.type: str = "Gate"
        self.gate_type: str = "XOR"

        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0]
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()