import arcade
from typing import List, Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.id_generator import random_id

from modules.data import data
from modules.data.level import Level


from modules.ui.editor.view import EditorView
from modules.ui.level_player.selector import LevelPlayerSelector

"""
Provides the LevelEditorSelector class for managing level selection and creation
workflows within the arcade application.
"""


class LevelEditorSelector(arcade.View):
    """
    Manages the UI view for browsing existing levels or creating new ones.
    """

    def __init__(self) -> None:
        """
        Initializes the view with default background and container structures.
        """
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []
        self.levels: List[Any] = []
        self.camera: int = 0
        self.setup()

    def setup(self) -> None:
        """
        Populates the UI labels and initializes interaction objects for levels.
        """
        debug_list: List[str] = [
            "Level Editor Selector",
            "<- Back",
            "+ New +",
            "Play Level Selector",
            "",
        ]
        self.texts: List[Text] = []
        self.levels: List[Any] = []
        

        for i in data.loaded_levels:
            level = data.loaded_levels[i]
            debug_list.append(f"Level {level.number} {level.name} #{level.id}")
            self.levels.append(i)

        start_y: int = data.WINDOW_HEIGHT - 70 + self.camera

        for index, item in enumerate(debug_list):
            self.texts.append(Text())
            self.texts[-1].x = 64
            self.texts[-1].y = start_y - (index * 25)
            self.texts[-1].text = item
            self.texts[-1].align = ("left", "center")

    def reset(self) -> None:
        """
        Resets the current view state.
        """
        pass

    def on_draw(self) -> None:
        """
        Renders all UI text elements and their associated hitboxes.
        """
        self.clear()

        for i in self.texts:
            i.draw()
            i.hitbox.draw()

    def on_update(self, delta_time: float) -> None:
        """
        Updates logic state per frame.

        Args:
            delta_time: Time elapsed since the previous update.
        """
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """
        Handles keyboard input events.

        Args:
            key: Integer identifier of the pressed key.
            key_modifiers: Bitmask of modifier keys currently held.
        """
        if key == 97:
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """
        Handles key release events.

        Args:
            key: Integer identifier of the released key.
            key_modifiers: Bitmask of modifier keys currently held.
        """
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """
        Updates the global mouse tracking state.

        Args:
            x: Current horizontal mouse position.
            y: Current vertical mouse position.
            delta_x: Change in x position.
            delta_y: Change in y position.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Triggers UI navigation based on interaction with text element hitboxes.

        Args:
            x: Current horizontal mouse position.
            y: Current vertical mouse position.
            button: Identifier of the pressed mouse button.
            key_modifiers: Bitmask of modifier keys currently held.
        """
        for index in range(len(self.texts)):
            text = self.texts[index]

            if text.touched:
                if index > 4:
                    data.window.display(
                        EditorView(level=data.loaded_levels[self.levels[index - 5]])
                    )
                elif index == 1:
                    data.window.back()
                elif index == 2:
                    data.window.display(EditorView(level=Level(random_id())))
                elif index == 3:
                    data.window.display(LevelPlayerSelector())

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Handles mouse release events.

        Args:
            x: Current horizontal mouse position.
            y: Current vertical mouse position.
            button: Identifier of the released mouse button.
            key_modifiers: Bitmask of modifier keys currently held.
        """
        pass
    def on_mouse_scroll(
        self, x: float, y: float, scroll_x: float, scroll_y: float
    ) -> None:
        """Updates vertical camera offset and rebuilds layout."""
        self.camera += scroll_y * -data.MOUSE_SENSI
        self.camera = max(self.camera, 0)

        self.setup()