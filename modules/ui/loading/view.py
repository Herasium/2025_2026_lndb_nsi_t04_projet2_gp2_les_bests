import arcade
import data

class LoadingScreen(arcade.View):
    """
    Représente l'écran de chargement de l'application.
    Gère l'affichage visuel et la logique de transition lors de l'initialisation des ressources.
    """
    
    def __init__(self) -> None:
        # Initialisation de la classe parente arcade.View
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK

    def reset(self) -> None:
        """Réinitialise l'état de l'écran de chargement."""
        pass

    def on_draw(self) -> None:
        """Rendu de l'écran."""
        self.clear()

        # Affichage du texte de chargement au centre de la fenêtre
        arcade.draw_text(
            "Chargement en cours", data.WINDOW_WIDTH / 2, data.WINDOW_HEIGHT / 2, arcade.color.WHITE
        )

    def on_update(self, delta_time: float) -> None:
        """
        Logique de mise à jour de l'écran.
        
        :param delta_time: Temps écoulé depuis la dernière mise à jour.
        """
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Gère les entrées clavier de l'utilisateur."""
        # Si la touche 'a' (code 97) est pressée, quitter l'application
        if key == 97:
            arcade.exit()

    def on_mouse_motion(self, x, y, dx, dy):
        """Gère les mouvements de la souris."""
        pass