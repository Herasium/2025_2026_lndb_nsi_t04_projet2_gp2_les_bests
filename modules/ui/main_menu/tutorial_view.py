import arcade
from typing import List

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.toolbox.text import Text

from modules.data import data


class TutorialView(arcade.View):
    """
    View class representing the tutorial interface.
    """

    def __init__(self) -> None:
        """
        Initialize the TutorialView, setting up UI components and buttons.
        """
        super().__init__()

        self.background_color = arcade.color.JET

        # UI elements
        self.name_banner_sprite = data.name_banner

        # Setup back navigation button
        self.back_button = Button()
        self.back_button.x = 192 / 2.5 - 30
        self.back_button.y = 1010 + 10
        self.back_button.width = 80
        self.back_button.height = 40

        # Title and header text labels
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

        # Main selection buttons as Text elements
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

        # Dynamic list of tutorial sub-buttons
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
            a = a - 45  # Offset position for each subsequent button
            self.buttons.append(
                Text(
                    x=160,
                    y=a,
                    text=data.language.get("tutorial", i),
                    align=("left", "center"),
                    size=16,
                )
            )

        # Text display area for tutorial content
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
        """
        Handle keyboard inputs.

        Parameters:
        - key: integer representation of the key pressed
        - key_modifiers: bitwise flags for modifier keys (Ctrl, Alt, etc.)
        """
        if key == 97:  # "a" key to exit application
            arcade.exit()

    def draw_tile(self, id: int, x: float, y: float) -> None:
        """
        Draw a UI tile from the sprite sheet at a given location.

        Parameters:
        - id: index of the tile texture
        - x: x-coordinate
        - y: y-coordinate
        """
        rect = arcade.XYWH(x=x, y=y, width=64, height=64, anchor=arcade.Vec2(0, 0))

        arcade.draw_texture_rect(data.ui_border_tiles[id], rect)

    def draw_frame_border(self) -> None:
        """
        Draw the decorative UI border surrounding the tutorial window.
        """
        start_x = 32
        start_y = 865
        y_len = 13
        x_len = 28

        # Draw top border segments
        self.draw_tile(0, start_x, start_y)
        for i in range(x_len - 1):
            self.draw_tile(1, start_x + (i + 1) * 64, start_y)
        self.draw_tile(3, start_x + x_len * 64, start_y)

        # Draw side borders
        for i in range(y_len - 1):
            self.draw_tile(4, start_x, start_y - (i + 1) * 64)
            self.draw_tile(7, start_x + x_len * 64, start_y - (i + 1) * 64)

        # Draw bottom border segments
        self.draw_tile(12, start_x, start_y - y_len * 64)
        self.draw_tile(13, start_x + 64, start_y - y_len * 64)
        self.draw_tile(5, start_x + 2 * 64, start_y - y_len * 64)
        self.draw_tile(6, start_x + 3 * 64, start_y - y_len * 64)
        self.draw_tile(10, start_x + 4 * 64, start_y - y_len * 64)
        for i in range(x_len - 5):
            self.draw_tile(13, start_x + (i + 5) * 64, start_y - y_len * 64)
        self.draw_tile(15, start_x + x_len * 64, start_y - y_len * 64)

    def draw_frame_background(self) -> None:
        """
        Fill the background of the UI frame with repeated tiles.
        """
        start_x = 32
        start_y = 865 + 64
        y_len = 15

        for i in range(y_len - 1):
            for a in range(29):
                self.draw_tile(9, start_x + (a) * 64, start_y - (i + 1) * 64)

    def on_draw(self) -> None:
        """
        Render all UI components to the screen.
        """
        self.clear(arcade.color.BLACK)

        self.draw_frame_background()
        self.draw_frame_border()

        self.texte_button.draw()
        self.back_button.draw()

        self.regletexte.draw()
        self.listeportetexte.draw()

        self.regleplay_button.draw()
        self.commande_button.draw()

        # Render each button in the dynamic button list
        for i in self.buttons:
            i.draw()

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """
        Update global mouse position on movement.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Handle mouse clicks for UI interaction.
        """
        if self.back_button.touched:
            data.window.back()

        # Handle text display update for tutorial sections
        if self.regleplay_button.touched:
            self.texte_button.text = data.language.tutorial["button_01"]

        if self.commande_button.touched:
            self.texte_button.text = data.language.tutorial["button_02"]

        for i in self.buttons:
            if i.touched:
                pass  # Placeholder for future button functionality
