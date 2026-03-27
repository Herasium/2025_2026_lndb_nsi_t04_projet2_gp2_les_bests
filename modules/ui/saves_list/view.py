"""Fournit la vue SaveFrame pour l'édition et l'enregistrement des données de configuration des puces."""

import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.entity import Entity
from modules.data import data
from modules.ui.editor.view import EditorView


class ChipList(arcade.View):
    """Gère la disposition de l'interface utilisateur et les interactions pour l'édition des propriétés des puces."""

    def __init__(self) -> None:
        """Initialise l'instance de ChipList.

        Args:
            chip: L'objet de configuration contenant les données de la puce à modifier.
        """
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.camera = -70
        self.private_count = 0

        self.setup()

    def setup(self) -> None:

        self.back_button = Entity(
            x=1680, y=100, width=160, height=100, sprite=data.button_back
        )

        self.bg = Entity(
            0,
            0,
            data.WINDOW_WIDTH,
            (((data.WINDOW_HEIGHT + 32) // 64) * 64),
            arcade.Sprite(data.background_grid_texture),
        )
        self.border = Entity(0, 0, data.WINDOW_WIDTH, 960, data.border_small)
        self.title = Entity(0, 952, data.WINDOW_WIDTH, 128, data.name_banner)
        self.private_count = 0
        self.chips = []

        offset = 150

        for chip_id in data.loaded_chips:
            result = {}
            chip = data.loaded_chips[chip_id]
            if chip.private:
                self.private_count += 1
                continue
            i = len(self.chips) - self.private_count
            result["bg"] = Entity(
                x=400,
                y=800 - offset * i + self.camera,
                width=1120,
                height=125,
                sprite=data.chip_select,
            )
            result["name"] = Text(
                x=450,
                y=885 - offset * i + self.camera,
                width=920,
                height=30,
                text=chip.name,
                align=("left", "center"),
            )
            result["id"] = Text(
                x=450,
                y=840 - offset * i + self.camera,
                width=920,
                height=30,
                text=f"ID Puce :{chip.id}",
                align=("left", "center"),
                size=12,
            )
            result["button"] = Entity(
                x=data.WINDOW_WIDTH / 2 + 510 - 144,
                y=820 - offset * i + self.camera,
                width=144,
                height=90,
                sprite=data.button_edit,
            )
            result["index"] = i
            result["chip_id"] = chip_id
            self.chips.append(result)

        self.new = Entity(
            x=data.WINDOW_WIDTH / 2 - 216 / 2,
            y=800
            - offset * (len(data.loaded_chips) - self.private_count)
            + self.camera,
            width=216,
            height=128,
            sprite=data.button_new,
        )

    def move(self) -> None:
        offset = 150
        for a in self.chips:
            i = a["index"]

            a["bg"].y = 800 - offset * i + self.camera
            a["name"].y = 885 - offset * i + self.camera
            a["id"].y = 840 - offset * i + self.camera
            a["button"].y = 820 - offset * i + self.camera
        self.new.y = (
            800 - offset * (len(data.loaded_chips) - self.private_count) + self.camera
        )

    def on_mouse_scroll(
        self, x: float, y: float, scroll_x: float, scroll_y: float
    ) -> None:
        """Met à jour le décalage vertical de la caméra et reconstruit la disposition."""
        self.camera += scroll_y * -data.MOUSE_SENSI
        self.camera = max(self.camera, -70)
        self.move()

    def reset(self) -> None:
        """Réinitialise l'état interne de la vue."""
        pass

    def on_draw(self) -> None:
        """Rend tous les éléments textuels de l'interface configurés."""
        self.clear()
        self.bg.draw()

        for i in self.chips:
            i["bg"].draw()
            i["name"].draw()
            i["id"].draw()
            i["button"].draw()

        self.new.draw()
        self.border.draw()
        self.title.draw()
        self.back_button.draw()

    def on_update(self, delta_time: float) -> None:
        """Gère les mises à jour logiques périodiques."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Gère les événements de pression de touches du clavier.

        Args:
            key: L'identifiant de la touche pressée.
            key_modifiers: Drapeaux binaires pour les touches de modification.
        """
        if key == data.keys.back:
            data.window.display(data.main)
        if key == 65473:  # Sortie de secours : F4
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Gère les événements de relâchement de touches."""
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Met à jour l'état global du suivi de la souris.

        Args:
            x: La coordonnée x actuelle de la souris.
            y: La coordonnée y actuelle de la souris.
            delta_x: La variation de la coordonnée x depuis la dernière image.
            delta_y: La variation de la coordonnée y depuis la dernière image.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Traite les interactions de clic de souris avec les éléments de l'interface.

        Args:
            x: La coordonnée x du clic de souris.
            y: La coordonnée y du clic de souris.
            button: Le bouton de la souris pressé.
            key_modifiers: Drapeaux binaires pour les touches de modification.
        """
        for i in self.chips:
            if i["button"].touched:
                data.window.display(EditorView(id=i["chip_id"]))
        if self.new.touched:
            data.window.display(EditorView())

        if self.back_button.touched:
            data.window.display(data.main)

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Gère les événements de relâchement du bouton de la souris."""
        pass