import arcade
from typing import List

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.entity import Entity

from modules.data import data

"""Fournit l'interface pour la section tutoriel de l'application."""


class TutorialView(arcade.View):
    """Gère la disposition, le rendu et la logique d'interaction pour l'écran du tutoriel."""

    def __init__(self) -> None:
        """Initialise la vue, les éléments de l'interface utilisateur et les positions de mise en page."""
        super().__init__()

        self.camera = 0

        self.background_color = arcade.color.JET

        self.name_banner_sprite = data.name_banner

        self.bg = Entity(
            0,
            0,
            data.WINDOW_WIDTH,
            (((data.WINDOW_HEIGHT + 32) // 64) * 64),
            arcade.Sprite(data.background_grid_texture),
        )
        self.border = Entity(0, 0, data.WINDOW_WIDTH, 960, data.border_small)
        self.title = Entity(0, 952, data.WINDOW_WIDTH, 128, data.name_banner)

        self.back_button = Entity(
            x=1654, y=100, width=160, height=100, sprite=data.button_back
        )


        self.setup_texts()

        self.texte_button = Text(
            x=1000,
            y=800,
            text="",
            align=("left", "top"),
            size=16,
            multiline=True,
            width=750,
        )

        self.porte_actuelle = 0

        self.and_truth = Entity(
            x=1065,
            y=20,
            width=620,
            height=620,
            sprite=data.tuto_truth["and"],
        )
        self.not_truth = Entity(
            x=1065,
            y=20,
            width=620,
            height=620,
            sprite=data.tuto_truth["not"],
        )
        self.or_truth = Entity(
            x=1065,
            y=20,
            width=620,
            height=620,
            sprite=data.tuto_truth["or"],
        )
        self.nand_truth = Entity(
            x=1065,
            y=20,
            width=620,
            height=620,
            sprite=data.tuto_truth["nand"],
        )
        self.nor_truth = Entity(
            x=1065,
            y=20,
            width=620,
            height=620,
            sprite=data.tuto_truth["nor"],
        )
        self.xor_truth = Entity(
            x=1065,
            y=20,
            width=620,
            height=620,
            sprite=data.tuto_truth["xor"],
        )

    def setup_texts(self) -> None:
        self.regletexte = Text(
            x=120,
            y=820 + self.camera,
            text=data.language.get("tutorial", "title_1"),
            align=("left", "center"),
        )
        self.listeportetexte = Text(
            x=120,
            y=600 + self.camera,
            text=data.language.get("tutorial", "title_2"),
            align=("left", "center"),
        )
        self.listeportetextebits = Text(
            x=120,
            y=30 + self.camera,
            text=data.language.get("tutorial", "title_3"),
            align=("left", "center"),
        )

        self.regleplay_button = Text(
            x=160,
            y=740 + self.camera,
            text=data.language.get("tutorial", "button_1"),
            align=("left", "center"),
            size=16,
        )
        self.commande_button = Text(
            x=160,
            y=685 + self.camera,
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
        self.bitsbutton: List[str] = [
            "button_13",
            "button_14",
            "button_14",
        ]

        # Ajouter MAKER, ON, BREAKER

        self.buttons: List[Text] = []

        a = 560
        for i in self.namebutton:
            a = a - 45
            self.buttons.append(
                Text(
                    x=160,
                    y=a + self.camera,
                    text=data.language.get("tutorial", i),
                    align=("left", "center"),
                    size=16,
                )
            )

        b = 0
        for i in self.bitsbutton:
            b = b - 45
            self.buttons.append(
                Text(
                    x=160,
                    y=b + self.camera,
                    text=data.language.get("tutorial", i),
                    align=("left", "center"),
                    size=16,
                )
            )

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Gère les événements de saisie au clavier.

        Args:
            key: Le code de la touche pressée.
            key_modifiers: Drapeaux binaires indiquant les touches de modification actives.
        """
        if key == data.keys.back:
            data.window.display(data.main)
        if key == 65473:  # Sortie d'urgence : F4
            arcade.exit()


    def on_draw(self) -> None:
        """Affiche l'état actuel de la vue à l'écran."""
        self.clear(arcade.color.BLACK)

        self.bg.draw()

        self.texte_button.draw()
        self.back_button.draw()

        self.regletexte.draw()
        self.listeportetexte.draw()
        self.listeportetextebits.draw()

        self.regleplay_button.draw()
        self.commande_button.draw()

        for i in self.buttons:
            i.draw()

        if self.porte_actuelle == 2:
            self.and_truth.draw()
        if self.porte_actuelle == 3:
            self.not_truth.draw()
        if self.porte_actuelle == 4:
            self.or_truth.draw()
        if self.porte_actuelle == 5:
            self.nand_truth.draw()
        if self.porte_actuelle == 6:
            self.nor_truth.draw()
        if self.porte_actuelle == 7:
            self.xor_truth.draw()

        self.border.draw()
        self.title.draw()

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Met à jour l'état global du suivi de la souris.

        Args:
            x: Position horizontale actuelle de la souris.
            y: Position verticale actuelle de la souris.
            delta_x: Mouvement horizontal depuis la dernière image.
            delta_y: Mouvement vertical depuis la dernière image.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Traite les événements d'interaction de la souris pour les éléments de l'interface.

        Args:
            x: Position horizontale de la souris au moment du clic.
            y: Position verticale de la souris au moment du clic.
            button: Le bouton de la souris pressé.
            key_modifiers: Drapeaux binaires pour les touches de modification actives.
        """
        if self.back_button.touched:
            data.window.display(data.main)

        if self.regleplay_button.touched:
            self.porte_actuelle = 0
            self.texte_button.text = data.language.tutorial["button_01"]

        if self.commande_button.touched:
            self.porte_actuelle = 0
            self.texte_button.text = data.language.tutorial["button_02"]

        for i in self.buttons:
            p = self.buttons.index(i)
            if i.touched:
                self.porte_actuelle = p
                keys = list(data.language.tutorial.keys())
                ask_key = keys[p + 20]
                self.texte_button.text = data.language.tutorial[ask_key]

    def on_mouse_scroll(
        self, x: float, y: float, scroll_x: float, scroll_y: float
    ) -> None:
        """Met à jour le décalage vertical de la caméra et reconstruit la mise en page."""
        self.camera += scroll_y * -data.MOUSE_SENSI
        self.camera = max(self.camera, 0)
        self.setup_texts()