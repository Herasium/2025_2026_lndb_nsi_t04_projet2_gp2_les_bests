import arcade
import math


class LoadingScreen(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK

        # Loading text animation
        self.loading_base_text = "Loading"
        self.loading_dots = 0
        self.loading_timer = 0

        # Spinner animation
        self.angle = 0

    def reset(self) -> None:
        self.loading_dots = 0
        self.loading_timer = 0
        self.angle = 0

    def on_draw(self) -> None:
        self.clear()

        width = self.window.width
        height = self.window.height

        # ---- Loading text ----
        dots = "." * self.loading_dots
        text = f"{self.loading_base_text}{dots}"

        arcade.draw_text(
            text,
            width / 2,
            height / 2 + 40,
            arcade.color.WHITE,
            24,
            anchor_x="center",
        )

        # ---- Spinner (rotating arc) ----
        radius = 30
        center_x = width / 2
        center_y = height / 2 - 20

        # Draw rotating arc
        arcade.draw_arc_outline(
            center_x,
            center_y,
            radius * 2,
            radius * 2,
            arcade.color.WHITE,
            start_angle=self.angle,
            end_angle=self.angle + 270,  # not full circle → looks like spinner
            border_width=4,
        )

    def on_update(self, delta_time: float) -> None:
        # ---- Animate dots ----
        self.loading_timer += delta_time
        if self.loading_timer > 0.5:
            self.loading_timer = 0
            self.loading_dots = (self.loading_dots + 1) % 4  # 0 → 3 dots

        # ---- Rotate spinner ----
        self.angle += 180 * delta_time  # degrees per second
        self.angle %= 360

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        if key == 97:
            arcade.exit()

    def on_mouse_motion(self, x, y, dx, dy):
        pass