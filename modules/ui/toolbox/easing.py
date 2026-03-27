"""
Une bibliothèque fournissant diverses fonctions d'atténuation (easing) mathématiques pour les séquences d'animation.

Ce module implémente des courbes d'interpolation standard pour créer des transitions
fluides et naturelles entre une valeur de départ et une valeur de fin sur une durée définie.
"""

import math


class EasingBase:
    """Interface de base pour l'implémentation de transitions d'atténuation spécifiques."""

    def __init__(self, start: float = 0, end: float = 1, duration: int = 100) -> None:
        """Initialise l'état de base de l'atténuation.

        Args:
            start: La valeur initiale de l'animation.
            end: La valeur cible de l'animation.
            duration: Le nombre total d'itérations pour terminer la transition.
        """
        self.start: float = start
        self.end: float = end
        self.duration: int = duration
        self.current: int = 0
        self.done: bool = False

    def func(self) -> float:
        """Calcule le facteur de progression normalisé.

        Returns:
            Le scalaire de progression entre 0.0 et 1.0.
        """
        raise NotImplementedError

    def tick(self) -> float:
        """Avance l'état interne d'une étape et calcule la valeur actuelle.

        Returns:
            La valeur interpolée à l'étape actuelle de la chronologie.
        """
        if self.current < self.duration:
            value: float = self.func()
            self.current += 1
            return self.start + (self.end - self.start) * value
        else:
            self.done = True
            return self.end

    def reset(self) -> None:
        """Réinitialise l'état de l'animation à la position initiale."""
        self.current = 0
        self.done = False


class LinearInOut(EasingBase):
    """Effectue une interpolation linéaire entre le début et la fin."""

    def func(self) -> float:
        """Calcule l'atténuation linéaire."""
        t: float = self.current / self.duration
        return t


class QuadEaseInOut(EasingBase):
    """Effectue une interpolation quadratique de type ease-in-out."""

    def func(self) -> float:
        """Calcule l'atténuation quadratique In-Out."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 2 * t * t
        return (-2 * t * t) + (4 * t) - 1


class QuadEaseIn(EasingBase):
    """Effectue une interpolation quadratique de type ease-in."""

    def func(self) -> float:
        """Calcule l'atténuation quadratique In."""
        t: float = self.current / self.duration
        return t * t


class QuadEaseOut(EasingBase):
    """Effectue une interpolation quadratique de type ease-out."""

    def func(self) -> float:
        """Calcule l'atténuation quadratique Out."""
        t: float = self.current / self.duration
        return -(t * (t - 2))


class CubicEaseIn(EasingBase):
    """Effectue une interpolation cubique de type ease-in."""

    def func(self) -> float:
        """Calcule l'atténuation cubique In."""
        t: float = self.current / self.duration
        return t * t * t


class CubicEaseOut(EasingBase):
    """Effectue une interpolation cubique de type ease-out."""

    def func(self) -> float:
        """Calcule l'atténuation cubique Out."""
        t: float = self.current / self.duration
        return (t - 1) * (t - 1) * (t - 1) + 1


class CubicEaseInOut(EasingBase):
    """Effectue une interpolation cubique de type ease-in-out."""

    def func(self) -> float:
        """Calcule l'atténuation cubique In-Out."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 4 * t * t * t
        p: float = 2 * t - 2
        return 0.5 * p * p * p + 1


class QuarticEaseIn(EasingBase):
    """Effectue une interpolation quartique de type ease-in."""

    def func(self) -> float:
        """Calcule l'atténuation quartique In."""
        t: float = self.current / self.duration
        return t * t * t * t


class QuarticEaseOut(EasingBase):
    """Effectue une interpolation quartique de type ease-out."""

    def func(self) -> float:
        """Calcule l'atténuation quartique Out."""
        t: float = self.current / self.duration
        return (t - 1) * (t - 1) * (t - 1) * (1 - t) + 1


class QuarticEaseInOut(EasingBase):
    """Effectue une interpolation quartique de type ease-in-out."""

    def func(self) -> float:
        """Calcule l'atténuation quartique In-Out."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 8 * t * t * t * t
        p: float = t - 1
        return -8 * p * p * p * p + 1


class QuinticEaseIn(EasingBase):
    """Effectue une interpolation quintique de type ease-in."""

    def func(self) -> float:
        """Calcule l'atténuation quintique In."""
        t: float = self.current / self.duration
        return t * t * t * t * t


class QuinticEaseOut(EasingBase):
    """Effectue une interpolation quintique de type ease-out."""

    def func(self) -> float:
        """Calcule l'atténuation quintique Out."""
        t: float = self.current / self.duration
        return (t - 1) * (t - 1) * (t - 1) * (t - 1) * (t - 1) + 1


class QuinticEaseInOut(EasingBase):
    """Effectue une interpolation quintique de type ease-in-out."""

    def func(self) -> float:
        """Calcule l'atténuation quintique In-Out."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 16 * t * t * t * t * t
        p: float = (2 * t) - 2
        return 0.5 * p * p * p * p * p + 1


class SineEaseIn(EasingBase):
    """Effectue une interpolation sinusoïdale de type ease-in."""

    def func(self) -> float:
        """Calcule l'atténuation sinusoïdale In."""
        t: float = self.current / self.duration
        return math.sin((t - 1) * math.pi / 2) + 1


class SineEaseOut(EasingBase):
    """Effectue une interpolation sinusoïdale de type ease-out."""

    def func(self) -> float:
        """Calcule l'atténuation sinusoïdale Out."""
        t: float = self.current / self.duration
        return math.sin(t * math.pi / 2)


class SineEaseInOut(EasingBase):
    """Effectue une interpolation sinusoïdale de type ease-in-out."""

    def func(self) -> float:
        """Calcule l'atténuation sinusoïdale In-Out."""
        t: float = self.current / self.duration
        return 0.5 * (1 - math.cos(t * math.pi))


class CircularEaseIn(EasingBase):
    """Effectue une interpolation circulaire de type ease-in."""

    def func(self) -> float:
        """Calcule l'atténuation circulaire In."""
        t: float = self.current / self.duration
        return 1 - math.sqrt(1 - (t * t))


class CircularEaseOut(EasingBase):
    """Effectue une interpolation circulaire de type ease-out."""

    def func(self) -> float:
        """Calcule l'atténuation circulaire Out."""
        t: float = self.current / self.duration
        return math.sqrt((2 - t) * t)


class CircularEaseInOut(EasingBase):
    """Effectue une interpolation circulaire de type ease-in-out."""

    def func(self) -> float:
        """Calcule l'atténuation circulaire In-Out."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 0.5 * (1 - math.sqrt(1 - 4 * (t * t)))
        return 0.5 * (math.sqrt(-((2 * t) - 3) * ((2 * t) - 1)) + 1)


class ExponentialEaseIn(EasingBase):
    """Effectue une interpolation exponentielle de type ease-in."""

    def func(self) -> float:
        """Calcule l'atténuation exponentielle In."""
        t: float = self.current / self.duration
        if t == 0:
            return 0
        return math.pow(2, 10 * (t - 1))


class ExponentialEaseOut(EasingBase):
    """Effectue une interpolation exponentielle de type ease-out."""

    def func(self) -> float:
        """Calcule l'atténuation exponentielle Out."""
        t: float = self.current / self.duration
        if t == 1:
            return 1
        return 1 - math.pow(2, -10 * t)


class ExponentialEaseInOut(EasingBase):
    """Effectue une interpolation exponentielle de type ease-in-out."""

    def func(self) -> float:
        """Calcule l'atténuation exponentielle In-Out."""
        t: float = self.current / self.duration
        if t == 0 or t == 1:
            return t
        if t < 0.5:
            return 0.5 * math.pow(2, (20 * t) - 10)
        return -0.5 * math.pow(2, (-20 * t) + 10) + 1


class ElasticEaseIn(EasingBase):
    """Effectue une interpolation élastique de type ease-in."""

    def func(self) -> float:
        """Calcule l'atténuation élastique In."""
        t: float = self.current / self.duration
        return math.sin(13 * math.pi / 2 * t) * math.pow(2, 10 * (t - 1))


class ElasticEaseOut(EasingBase):
    """Effectue une interpolation élastique de type ease-out."""

    def func(self) -> float:
        """Calcule l'atténuation élastique Out."""
        t: float = self.current / self.duration
        return math.sin(-13 * math.pi / 2 * (t + 1)) * math.pow(2, -10 * t) + 1


class ElasticEaseInOut(EasingBase):
    """Effectue une interpolation élastique de type ease-in-out."""

    def func(self) -> float:
        """Calcule l'atténuation élastique In-Out."""
        t: float = self.current / self.duration
        if t < 0.5:
            return (
                0.5
                * math.sin(13 * math.pi / 2 * (2 * t))
                * math.pow(2, 10 * ((2 * t) - 1))
            )
        return 0.5 * (
            math.sin(-13 * math.pi / 2 * ((2 * t - 1) + 1))
            * math.pow(2, -10 * (2 * t - 1))
            + 2
        )


class BackEaseIn(EasingBase):
    """Effectue une atténuation de type back-in, avec un léger dépassement au début."""

    def func(self) -> float:
        """Calcule l'atténuation Back In."""
        t: float = self.current / self.duration
        return t * t * t - t * math.sin(t * math.pi)


class BackEaseOut(EasingBase):
    """Effectue une atténuation de type back-out, avec un léger dépassement à la fin."""

    def func(self) -> float:
        """Calcule l'atténuation Back Out."""
        t: float = self.current / self.duration
        p: float = 1 - t
        return 1 - (p * p * p - p * math.sin(p * math.pi))


class BackEaseInOut(EasingBase):
    """Effectue une atténuation de type back-in-out avec des dépassements aux deux extrémités."""

    def func(self) -> float:
        """Calcule l'atténuation Back In-Out."""
        t: float = self.current / self.duration
        if t < 0.5:
            p: float = 2 * t
            return 0.5 * (p * p * p - p * math.sin(p * math.pi))
        p: float = 1 - (2 * t - 1)
        return 0.5 * (1 - (p * p * p - p * math.sin(p * math.pi))) + 0.5


class BounceEaseIn(EasingBase):
    """Effectue une atténuation de type rebond (bounce-in)."""

    def func(self) -> float:
        """Calcule l'atténuation Bounce In en déléguant à BounceEaseOut."""
        t: float = self.current / self.duration
        n: BounceEaseOut = BounceEaseOut()
        n.current = 1 - t
        n.duration = 1
        return 1 - n.func()


class BounceEaseOut(EasingBase):
    """Effectue une atténuation de type rebond (bounce-out)."""

    def func(self) -> float:
        """Calcule l'atténuation Bounce Out en utilisant des fonctions par morceaux."""
        t: float = self.current / self.duration
        if t < 4 / 11:
            return 121 * t * t / 16
        elif t < 8 / 11:
            return (363 / 40.0 * t * t) - (99 / 10.0 * t) + 17 / 5.0
        elif t < 9 / 10:
            return (4356 / 361.0 * t * t) - (35442 / 1805.0 * t) + 16061 / 1805.0
        return (54 / 5.0 * t * t) - (513 / 25.0 * t) + 268 / 25.0


class BounceEaseInOut(EasingBase):
    """Effectue une atténuation de type rebond (bounce-in-out)."""

    def func(self) -> float:
        """Calcule l'atténuation Bounce In-Out."""
        t: float = self.current / self.duration
        if t < 0.5:
            n: BounceEaseIn = BounceEaseIn()
            n.current = t * 2
            n.duration = 1
            return 0.5 * n.func()
        n = BounceEaseOut()
        n.current = t * 2 - 1
        n.duration = 1
        return 0.5 * n.func() + 0.5