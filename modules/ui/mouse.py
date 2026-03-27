"""Fournit des capacités de suivi de la souris avec alignement sur la grille et analyse directionnelle."""

from typing import List, Tuple
from arcade import Vec2
from modules.data import data


class _Mouse:
    """Gère l'état de la souris, incluant la position brute, les coordonnées alignées sur la grille et les vecteurs de mouvement."""

    def __init__(self) -> None:
        """Initialise le traqueur de souris avec un état par défaut."""
        self._x: float = 0.0
        self._y: float = 0.0
        self._cursor: Vec2 = Vec2(0, 0)
        self._position: Tuple[float, float] = (0.0, 0.0)

        self.history: List[Vec2] = []
        self.direction: str = "RIGHT"
        self.previous_direction: str = "RIGHT"

        self.direction_bias: int = 0

        self._grid_size: int = data.UI_EDITOR_GRID_SIZE

    def _calculate_cursor(self) -> None:
        """Met à jour la position du curseur alignée sur la grille en fonction des coordonnées brutes actuelles."""
        self._cursor = Vec2(
            round(self._x / self._grid_size) * self._grid_size,
            round(self._y / self._grid_size) * self._grid_size,
        )

    def _calculate_direction(self) -> None:
        """Analyse l'historique récent des positions pour déterminer la direction actuelle du mouvement."""
        if len(self.history) > 4:
            self.history.pop(0)
            self.history.append(self.cursor)

            x1, y1 = self.history[0]
            x2, y2 = self.history[-1]

            dx: float = x2 - x1
            dy: float = y2 - y1

            self.previous_direction = self.direction

            if self.previous_direction == "RIGHT":
                dx += self.direction_bias
            if self.previous_direction == "LEFT":
                dx -= self.direction_bias

            if self.previous_direction == "UP":
                dy += self.direction_bias
            if self.previous_direction == "DOWN":
                dy -= self.direction_bias

            if abs(dx) >= abs(dy):
                self.direction = "RIGHT" if dx > 0 else "LEFT"
            else:
                self.direction = "UP" if dy > 0 else "DOWN"
        else:
            self.history.append(self.cursor)

    @property
    def position(self) -> Tuple[float, float]:
        """Retourne les coordonnées brutes de la souris."""
        return self._position

    @position.setter
    def position(self, value: Tuple[float, float]) -> Tuple[float, float]:
        """Met à jour la position brute de la souris et déclenche les calculs d'état dépendants.

        Args:
            value: Les coordonnées (x, y).

        Returns:
            Le tuple de position mis à jour.
        """
        self._position = value
        self._x = self._position[0]
        self._y = self._position[1]
        self._calculate_cursor()
        self._calculate_direction()
        return self._position

    @property
    def x(self) -> float:
        """Retourne la coordonnée x actuelle."""
        return self._x

    @property
    def y(self) -> float:
        """Retourne la coordonnée y actuelle."""
        return self._y

    @property
    def cursor(self) -> Vec2:
        """Retourne la position actuelle du curseur alignée sur la grille."""
        return self._cursor

    @property
    def grid_size(self) -> int:
        """Retourne la taille de grille active."""
        return self._grid_size

    @grid_size.setter
    def grid_size(self, value: int) -> None:
        """Met à jour la taille de la grille et ajuste la position alignée du curseur.

        Args:
            value: La taille de la grille en pixels.
        """
        self._grid_size = value
        self._calculate_cursor()


mouse: _Mouse = _Mouse()