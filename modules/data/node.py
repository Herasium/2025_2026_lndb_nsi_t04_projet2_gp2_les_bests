"""Fournit la classe de base Node pour les éléments de la boîte à outils de l'interface utilisateur."""

from typing import Any
from modules.ui.toolbox.entity import Entity


class Node:
    """Représente un élément structurel au sein du système de boîte à outils de l'interface utilisateur."""

    def __init__(self, id: Any) -> None:
        """Initialise le nœud avec un identifiant unique et un état par défaut.

        Args:
            id: L'identifiant unique à assigner à ce nœud.
        """
        self.entity: Entity = Entity()
        self.type: str = "DefaultNode"
        self.id: Any = id
        self._name: str = f"{self.type} ({self.id})"

    def draw(self) -> None:
        """Affiche le nœud dans l'interface utilisateur."""
        self.entity.draw()