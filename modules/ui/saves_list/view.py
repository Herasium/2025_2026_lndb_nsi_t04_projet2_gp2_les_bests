"""Provides the SaveFrame view for editing and saving chip configuration data."""

import arcade
from typing import Any, Dict, List

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.entity import Entity
from modules.ui.toolbox.keys import apply_key
from modules.data import data
from modules.ui.editor.view import EditorView


class ChipList(arcade.View):
    """Manages the UI layout and user interactions for editing chip properties."""

    def __init__(self) -> None:
        """Initializes the ChipList instance.

        Args:
            chip: The configuration object containing chip data to be modified.
        """
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.camera = -70

        self.setup()

    def setup(self) -> None:

        self.bg = Entity(0, 0, 1920, 1088, arcade.Sprite(data.background_grid_texture))
        self.border = Entity(0, 0, 1920, 960, data.border_small)
        self.title = Entity(0, 952, 1920, 128, data.name_banner)

        self.chips = []

        offset = 150

        for chip_id in data.loaded_chips:
            result = {}
            chip = data.loaded_chips[chip_id]
            i = len(self.chips)
            result["bg"] = Entity(x=400,y=800- offset*i + self.camera,width=1120,height=125,sprite=data.chip_select)
            result["name"] = Text(x=450,y=885 - offset*i  + self.camera,width=920,height=30,text=chip.name,align=("left","center"))
            result["id"] = Text(x=450,y=840 - offset*i  + self.camera,width=920,height=30,text=f"Chip Id:{chip.id}",align=("left","center"),size=12)
            result["button"] = Entity(x=1920/2+510-144,y=820-offset*i  + self.camera,width=144,height=90,sprite=data.button_edit)
            result["index"] = i
            result["chip_id"] = chip_id
            self.chips.append(result)

    def move(self) -> None:
        offset = 150
        for a in self.chips:
            i = a["index"]

            a["bg"].y = 800- offset*i + self.camera
            a["name"].y = 885 - offset*i  + self.camera
            a["id"].y = 840 - offset*i  + self.camera
            a["button"].y = 820-offset*i  + self.camera


    def on_mouse_scroll(
        self, x: float, y: float, scroll_x: float, scroll_y: float
    ) -> None:
        """Updates vertical camera offset and rebuilds layout."""
        self.camera += scroll_y * -data.MOUSE_SENSI
        self.camera = max(self.camera, -70)
        self.move()

    def reset(self) -> None:
        """Resets the internal state of the view."""
        pass

    def on_draw(self) -> None:
        """Renders all configured UI text elements."""
        self.clear()
        self.bg.draw()

        for i in self.chips:
            i["bg"].draw()
            i["name"].draw()
            i["id"].draw()
            i["button"].draw()

        self.border.draw()
        self.title.draw()


    def on_update(self, delta_time: float) -> None:
        """Handles periodic logic updates."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Handles keyboard input events.

        Args:
            key: The identifier of the pressed key.
            key_modifiers: Bitwise flags for modifier keys.
        """
        if key == 97:
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Handles key release events."""
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Updates the global mouse tracking state.

        Args:
            x: The current x-coordinate of the mouse.
            y: The current y-coordinate of the mouse.
            delta_x: The change in x-coordinate since the last frame.
            delta_y: The change in y-coordinate since the last frame.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Processes mouse click interactions with UI elements.

        Args:
            x: The x-coordinate of the mouse click.
            y: The y-coordinate of the mouse click.
            button: The mouse button pressed.
            key_modifiers: Bitwise flags for modifier keys.
        """
        for i in self.chips:
            if i["button"].touched:
                data.window.display(EditorView(id=i["chip_id"]))

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Handles mouse release events."""
        pass

