"""Fournit la classe CustomGate pour la gestion des instances de portes logiques définies par l'utilisateur."""

import arcade
from typing import Any, Dict, List, Optional
from line_profiler import profile

from modules.data.complex import Complex
from modules.data import data as data_module


class CustomGate(Complex):
    """Représente une porte logique définie par l'utilisateur enveloppant une architecture de puce interne."""

    def __init__(self, id: int, chip: Optional[Any] = None) -> None:
        """Initialise une nouvelle instance de CustomGate.

        Args:
            id: Identifiant unique pour la porte.
            chip: La définition de la puce à encapsuler.
        """
        super().__init__(id)

        self.name: str = chip.name
        self.type: str = "Custom"
        self.base_chip_id: int = chip.id
        self.chip: Any = chip.copy()
        self.gate_type: str = "Custom"
        self.safe_mode = False

        self.update_io()

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()

    def prop_io(self) -> None:
        """Propage les valeurs actuelles des entrées externes dans la structure interne de la puce."""
        chip_inputs: List[int] = self.chip.get_inputs()
        for i in range(len(self.inputs)):
            self.chip.gates[chip_inputs[i]].outputs[0] = self.inputs[i]

    def update_io(self) -> None:
        """Synchronise les broches d'E/S de la porte et les métadonnées du bus avec la puce sous-jacente."""
        self.inputs: List[int] = []
        self.outputs: List[int] = []
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = []

        chip_inputs: List[int] = self.chip.get_inputs()
        for i in chip_inputs:
            self.inputs.append(self.chip.gates[i].outputs[0] * 1)
            self.inputs_sizes.append(self.chip.gates[i].outputs_sizes[0])

        chip_outputs: List[int] = self.chip.get_outputs()
        for i in chip_outputs:
            self.outputs.append(self.chip.gates[i].inputs[0] * 1)
            self.outputs_sizes.append(self.chip.gates[i].inputs_sizes[0])

        self.update_text_readings()

    def draw_tiles(self) -> None:
        """Affiche la porte en utilisant des textures dépendantes de l'état actuel."""
        width: int = self.tile_width
        height: int = 4

        out: List[int] = self.outputs.copy()
        inp: List[int] = self.inputs.copy()

        for i in range(len(inp)):
            if self.inputs_sizes[i] != 1:
                inp[i] = 0

        for i in range(len(out)):
            if self.outputs_sizes[i] != 1:
                out[i] = 0

        out.reverse()
        inp.reverse()
        # Regroupe les bits d'état dans un entier pour sélectionner l'index de texture approprié
        if self.safe_mode:
            current: int = 0
        else:
            current: int = int("".join(map(str, map(int, (out + inp)))), 2)

        tile_x: float = self.x + self._camera[0]
        tile_y: float = self.y + self._camera[1]

        rect: arcade.XYWH = arcade.XYWH(
            x=tile_x,
            y=tile_y,
            width=width * data_module.UI_EDITOR_GRID_SIZE,
            height=height * data_module.UI_EDITOR_GRID_SIZE,
            anchor=arcade.Vec2(0, 0),
        )

        arcade.draw_texture_rect(
            data_module.IMAGE.get_texture(self.base_chip_id, current), rect
        )

        if not self.hide_text:
            for i in self.texts:
                self.texts[i].draw()

    def save(self) -> Dict[str, Any]:
        """Sérialise l'état de la porte pour le stockage.

        Returns:
            Dictionnaire contenant les données de configuration spatiale et logique.
        """
        return {
            "x": self.x,
            "y": self.y,
            "type": self.type,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "gate": self.gate_type,
            "id": self.id,
            "parent": self.base_chip_id,
        }

    @profile
    def load(self, data: Dict[str, Any]) -> None:
        """Restaure l'état de la porte à partir des données de configuration fournies.

        Args:
            data: Dictionnaire de configuration à charger.
        """
        self.type = data["type"]
        self.inputs = data.get("inputs", [])
        self.outputs = data.get("outputs", [])
        self.gate_type = data.get("gate", "")
        self.id = data["id"]
        self._x = data["x"]
        self._y = data["y"]
        self.base_chip_id = data["parent"]

        self.chip = data_module.loaded_chips[self.base_chip_id].copy()

        try:        
            out: List[int] = self.outputs.copy()
            inp: List[int] = self.inputs.copy()

            for i in range(len(inp)):
                if self.inputs_sizes[i] != 1:
                    inp[i] = 0

            for i in range(len(out)):
                if self.outputs_sizes[i] != 1:
                    out[i] = 0

            out.reverse()
            inp.reverse()
            a = int("".join(map(str, map(int, (out + inp)))), 2)
        except:
            self.safe_mode = True

        self.update_io()
        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()