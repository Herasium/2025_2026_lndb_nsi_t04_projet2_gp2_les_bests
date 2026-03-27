"""Fournit des mécanismes pour définir et gérer les éléments d'indice de l'interface utilisateur."""

from modules.data.chip import Chip


class Hint:
    """Représente un indice d'interface utilisateur configuré pour des formats d'affichage spécifiques.

    Attributs :
        chip : La représentation de données associée pour l'affichage basé sur les jetons (chips).
        text : Le contenu textuel principal affiché à l'utilisateur.
        type : Le mode de rendu où 0 est texte seul, 1 est jeton seul, et 2 est combiné.
        id : L'identifiant unique de cette instance.
    """

    def __init__(self, id: int) -> None:
        """Initialise l'instance de l'indice avec une configuration par défaut.

        Args :
            id : L'identifiant unique utilisé pour générer la référence interne du jeton.
        """
        self.chip: Chip = Chip(f"hint_chip_{id}")
        self.text: str = "Indice par défaut"
        self.type: int = 0
        self.id: int = id