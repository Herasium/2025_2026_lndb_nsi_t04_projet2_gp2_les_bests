import arcade
from typing import List

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.toolbox.text import Text

from modules.data import data

"""Provides the interface for the tutorial section of the application."""


class TutorialView(arcade.View):
    """Manages the layout, rendering, and interaction logic for the tutorial screen."""

    def __init__(self) -> None:
        """Initializes the view, UI elements, and layout positions."""
        super().__init__()

        self.background_color = arcade.color.JET

        self.name_banner_sprite = data.name_banner

        self.back_button = Button()
        self.back_button.x = 192 / 2.5 - 30
        self.back_button.y = 1010 + 10
        self.back_button.width = 80
        self.back_button.height = 40

        self.regletexte = Text(
            x=120,
            y=820,
            text=data.language.get("tutorial", "title_1"),
            align=("left", "center"),
        )
        self.listeportetexte = Text(
            x=120,
            y=600,
            text=data.language.get("tutorial", "title_2"),
            align=("left", "center"),
        )

        self.regleplay_button = Text(
            x=160,
            y=740,
            text=data.language.get("tutorial", "button_1"),
            align=("left", "center"),
            size=16,
        )
        self.commande_button = Text(
            x=160,
            y=685,
            text=data.language.get("tutorial", "button_2"),
            align=("left", "center"),
            size=16,
        )

        self.namebutton: List[str] = [
            "button_3",
            "button_4",
            "button_5",
            "button_6",
            "button_7",
            "button_8",
            "button_9",
            "button_10",
            "button_11",
            "button_12",
        ]
        self.buttons: List[Text] = []

        a = 560
        for i in self.namebutton:
            a = a - 45
            self.buttons.append(
                Text(
                    x=160,
                    y=a,
                    text=data.language.get("tutorial", i),
                    align=("left", "center"),
                    size=16,
                )
            )

        self.texte_button = Text(
            x=1000,
            y=750,
            text="",
            align=("left", "top"),
            size=16,
            multiline=True,
            width=750,
        )

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Handles keyboard input events.

        Args:
            key: The key code of the pressed key.
            key_modifiers: Bitwise flags indicating active modifier keys.
        """
        if key == 97:
            arcade.exit()

    def draw_tile(self, id: int, x: float, y: float) -> None:
        """Renders a single UI tile at the specified coordinates.

        Args:
            id: The index identifier for the texture to be drawn.
            x: The horizontal position on the screen.
            y: The vertical position on the screen.
        """
        rect = arcade.XYWH(x=x, y=y, width=64, height=64, anchor=arcade.Vec2(0, 0))

        arcade.draw_texture_rect(data.ui_border_tiles[id], rect)

    def draw_frame_border(self) -> None:
        """Renders the border components of the tutorial window."""
        start_x = 32
        start_y = 865
        y_len = 13
        x_len = 28

        self.draw_tile(0, start_x, start_y)
        for i in range(x_len - 1):
            self.draw_tile(1, start_x + (i + 1) * 64, start_y)
        self.draw_tile(3, start_x + x_len * 64, start_y)

        for i in range(y_len - 1):
            self.draw_tile(4, start_x, start_y - (i + 1) * 64)
            self.draw_tile(7, start_x + x_len * 64, start_y - (i + 1) * 64)

        self.draw_tile(12, start_x, start_y - y_len * 64)
        self.draw_tile(13, start_x + 64, start_y - y_len * 64)
        self.draw_tile(5, start_x + 2 * 64, start_y - y_len * 64)
        self.draw_tile(6, start_x + 3 * 64, start_y - y_len * 64)
        self.draw_tile(10, start_x + 4 * 64, start_y - y_len * 64)
        for i in range(x_len - 5):
            self.draw_tile(13, start_x + (i + 5) * 64, start_y - y_len * 64)
        self.draw_tile(15, start_x + x_len * 64, start_y - y_len * 64)

    def draw_frame_background(self) -> None:
        """Renders the background tiling for the UI frame."""
        start_x = 32
        start_y = 865 + 64
        y_len = 15

        for i in range(y_len - 1):
            for a in range(29):
                self.draw_tile(9, start_x + (a) * 64, start_y - (i + 1) * 64)

    def on_draw(self) -> None:
        """Renders the current view state to the display."""
        self.clear(arcade.color.BLACK)

        self.draw_frame_background()
        self.draw_frame_border()

        self.texte_button.draw()
        self.back_button.draw()

        self.regletexte.draw()
        self.listeportetexte.draw()

        self.regleplay_button.draw()
        self.commande_button.draw()

        for i in self.buttons:
            i.draw()

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Updates the global mouse tracking state.

        Args:
            x: Current horizontal mouse position.
            y: Current vertical mouse position.
            delta_x: Horizontal movement since last frame.
            delta_y: Vertical movement since last frame.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Processes mouse interaction events for UI elements.

        Args:
            x: Horizontal mouse position at time of click.
            y: Vertical mouse position at time of click.
            button: The mouse button being pressed.
            key_modifiers: Bitwise flags for active modifier keys.
        """
        if self.back_button.touched:
            data.window.back()

        if self.regleplay_button.touched:
            self.texte_button.text = data.language.tutorial["button_01"]

        if self.commande_button.touched:
            self.texte_button.text = data.language.tutorial["button_02"]

        for i in self.buttons:
            if i.touched:
                pass
