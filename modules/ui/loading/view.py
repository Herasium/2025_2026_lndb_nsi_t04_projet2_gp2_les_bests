import arcade
import data

class LoadingScreen(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK

    def reset(self) -> None:
        pass

    def on_draw(self) -> None:
        self.clear()

        arcade.draw_text(
            "Loading", data.WINDOW_WIDTH / 2, data.WINDOW_HEIGHT / 2, arcade.color.WHITE
        )

    def on_update(self, delta_time: float) -> None:
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        if key == 97:
            arcade.exit()

    def on_mouse_motion(self, x, y, dx, dy):
        pass
