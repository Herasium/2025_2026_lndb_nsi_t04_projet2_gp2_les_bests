"""Fournit les implémentations des portes logiques standard utilisées dans la simulation de circuits."""

from typing import List, Union

from modules.data.gate import Gate


class Nand(Gate):
    """Représente une porte logique NON-ET (NAND) dans une simulation de circuit."""

    def __init__(self, id: Union[int, str]) -> None:
        """Initialise la configuration de la porte NON-ET.

        Args:
            id: Identifiant unique de l'instance de la porte.
        """
        super().__init__(id)

        self.name: str = "NAND"
        self.type: str = "Gate"
        self.gate_type: str = "NAND"

        # Initialisation des entrées et sorties
        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [1]

        # Définition des dimensions des ports d'entrée et de sortie
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        # Calcul de l'affichage et génération du motif de la tuile
        self.calculate_display()
        self.gen_tile_pattern()