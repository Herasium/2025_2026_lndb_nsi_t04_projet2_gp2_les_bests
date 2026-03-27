import arcade

from modules.ui.mouse import mouse
from modules.data import data
from modules.ui.toolbox.keys import visual_key, apply_key
from modules.ui.toolbox.entity import Entity
from modules.ui.toolbox.text import Text


class SettingView(arcade.View):
    """Gère l'interface du menu des paramètres, incluant la disposition de l'interface utilisateur et les interactions avec l'utilisateur."""

    def __init__(self) -> None:
        """Initialise la vue, configure le positionnement des composants de l'interface et définit les ressources visuelles."""
        super().__init__()

        self.background_color: arcade.Color = arcade.color.JET

        self.camera = 0

        self.standart = 15

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

        self.writing = False
        self.single = False
        self.writing_value = ""
        self.current_selected = ""

        self.setup_texts()

    def write_value(self) -> None:

        if len(self.writing_value) != 0:
            match self.current_selected:
                case "max_framerate":
                    data.WINDOW_FRAMERATE = min(max(1, int(self.writing_value)), 1000)
                case "music_volume":
                    data.audio.music_volume = min(max(0, int(self.writing_value)), 100)
                case "sfx_volume":
                    data.audio.sfx_volume = min(max(0, int(self.writing_value)), 100)
                case "mouse_sensi":
                    data.MOUSE_SENSI = min(max(0, int(self.writing_value)), 255)

    def write_single(self) -> None:

        match self.current_selected:
            case "back":
                data.keys.back = self.writing_value
            case "input":
                data.keys.input_toggle = self.writing_value
            case "save":
                data.keys.chip_save = self.writing_value
            case "delete":
                data.keys.gate_delete = self.writing_value

    def text_list(self) -> None:

        self.texts = [
            ["--> Video <--", 30, "", False, False],
            ["Click to edit / toggle any values.", self.standart, "", False, False],
            [
                f"Resolution: {data.WINDOW_WIDTH}x{data.WINDOW_HEIGHT} (Fixed)",
                self.standart,
                "",
                False,
                False,
            ],
            [f"Fullscreen: {data.WINDOW_FULLSCREEN}", self.standart, "", False, False],
            [
                f"Max Framerate: {data.WINDOW_FRAMERATE} FPS",
                self.standart,
                "max_framerate",
                True,
                False,
            ],
            ["--> Audio <--", 30, "", False, False],
            [
                f"Music Volume: {data.audio.music_volume}",
                self.standart,
                "music_volume",
                True,
                False,
            ],
            [
                f"SFX Volume: {data.audio.sfx_volume}",
                self.standart,
                "sfx_volume",
                True,
                False,
            ],
            [f"Mute: {data.audio.mute}", self.standart, "", False, False],
            ["--> Inputs <--", 30, "", False, False],
            [
                f"Menu Back / Cancel: {data.keys.back} ({visual_key(data.keys.back)})",
                self.standart,
                "back",
                False,
                True,
            ],
            [
                f"Input Toggle: {data.keys.input_toggle} ({visual_key(data.keys.input_toggle)})",
                self.standart,
                "input",
                False,
                True,
            ],
            [
                f"Save Chip: {data.keys.chip_save} ({visual_key(data.keys.chip_save)})",
                self.standart,
                "save",
                False,
                True,
            ],
            [
                f"Mouse Sensitivity: {data.MOUSE_SENSI}",
                self.standart,
                "mouse_sensi",
                True,
                False,
            ],
            [
                f"Delete Gate: {data.keys.gate_delete} ({visual_key(data.keys.gate_delete)})",
                self.standart,
                "delete",
                False,
                True,
            ],
        ]

    def setup_texts(self) -> None:
        self.text_list()
        self.visual = []
        self.option_title = Entity(
            data.WINDOW_WIDTH / 2 - 896 / 2,
            700 + self.camera,
            896,
            128,
            data.option_title,
        )
        offset = 0
        index = 1
        for i in self.texts:
            align = ("left", "center")
            x = data.WINDOW_WIDTH / 2 - 400

            if i[1] != self.standart:
                align = ("center", "center")
                x = data.WINDOW_WIDTH / 2

            self.visual.append(
                Text(
                    x=x,
                    y=650 - offset + self.camera,
                    width=800,
                    height=50,
                    text=i[0],
                    size=i[1],
                    align=align,
                )
            )

            if self.writing and self.current_selected == i[2]:
                self.visual[-1].text = i[0].split(":")[0] + f": {self.writing_value}"

            if index != len(self.texts):
                if i[1] != self.standart or self.texts[index][1] != self.standart:
                    offset += 100
                else:
                    offset += 50
            index += 1

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Traite les entrées clavier.

        Args:
            key: Le code numérique de la touche pressée.
            key_modifiers: Drapeaux binaires pour les touches de modification maintenues.
        """
        if key == 65293:
            if self.writing:
                self.writing = False
                self.setup_texts()
        if key == data.keys.back:
            data.save()
            data.window.display(data.main)
        if key == 65473:  # Arrêt d'urgence : F4
            arcade.exit()

        if self.writing:
            self.writing_value = apply_key(
                self.writing_value, key, key_modifiers, int_only=True
            )
            self.write_value()
            self.setup_texts()

        if self.single:
            self.writing_value = key
            self.single = False
            self.write_single()
            self.setup_texts()

    def on_draw(self) -> None:
        """Effectue le rendu de la pile complète des vues."""
        self.clear(arcade.color.BLACK)

        self.bg.draw()

        self.option_title.draw()

        for i in self.visual:
            i.draw()

        self.border.draw()
        self.title.draw()

        self.back_button.draw()

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Synchronise l'état global de la souris avec la position actuelle du curseur.

        Args:
            x: Position horizontale actuelle du curseur.
            y: Position verticale actuelle du curseur.
            delta_x: Mouvement horizontal relatif à la dernière image.
            delta_y: Mouvement vertical relatif à la dernière image.
        """
        mouse.position = (x, y)

    def on_mouse_scroll(
        self, x: float, y: float, scroll_x: float, scroll_y: float
    ) -> None:
        """Met à jour le décalage vertical de la caméra et reconstruit la mise en page."""
        self.camera += scroll_y * -data.MOUSE_SENSI
        self.camera = max(self.camera, 0)
        self.setup_texts()

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Traite les clics de souris pour déclencher la navigation ou des événements d'action.

        Args:
            x: Position horizontale du curseur au moment du clic.
            y: Position verticale du curseur au moment du clic.
            button: Le bouton spécifique actionné.
            key_modifiers: Drapeaux binaires pour les touches de modification maintenues.
        """
        if self.back_button.touched:
            data.save()
            data.window.display(data.main)

        for i in range(len(self.visual)):
            if self.visual[i].touched:
                self.current_selected = self.texts[i][2]
                self.writing_value = ""
                self.writing = self.texts[i][3]
                self.single = self.texts[i][4]

                if i == 3:
                    data.WINDOW_FULLSCREEN = not data.WINDOW_FULLSCREEN
                if i == 8:
                    data.audio.mute = not data.audio.mute

        self.setup_texts()