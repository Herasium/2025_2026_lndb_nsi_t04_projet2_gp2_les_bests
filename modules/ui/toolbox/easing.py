"""
A library providing various mathematical easing functions for animation sequences.

This module implements standard interpolation curves to create natural-feeling
transitions between a start and end value over a defined duration.
"""

import math


class EasingBase:
    """Base interface for implementing specific easing transitions."""

    def __init__(self, start: float = 0, end: float = 1, duration: int = 100) -> None:
        """Initializes the base easing state.

        Args:
            start: The beginning value of the animation.
            end: The target value of the animation.
            duration: The total number of iterations to complete the transition.
        """
        self.start: float = start
        self.end: float = end
        self.duration: int = duration
        self.current: int = 0
        self.done: bool = False

    def func(self) -> float:
        """Calculates the normalized progress factor.

        Returns:
            The progression scalar between 0.0 and 1.0.
        """
        raise NotImplementedError

    def tick(self) -> float:
        """Advances the internal state by one step and computes the current value.

        Returns:
            The interpolated value at the current step in the timeline.
        """
        if self.current < self.duration:
            value: float = self.func()
            self.current += 1
            return self.start + (self.end - self.start) * value
        else:
            self.done = True
            return self.end

    def reset(self) -> None:
        """Resets the animation state to the initial position."""
        self.current = 0
        self.done = False


class LinearInOut(EasingBase):
    """Performs linear interpolation between start and end."""

    def func(self) -> float:
        """Calculates linear easing."""
        t: float = self.current / self.duration
        return t


class QuadEaseInOut(EasingBase):
    """Performs quadratic ease-in-out interpolation."""

    def func(self) -> float:
        """Calculates quadratic In-Out easing."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 2 * t * t
        return (-2 * t * t) + (4 * t) - 1


class QuadEaseIn(EasingBase):
    """Performs quadratic ease-in interpolation."""

    def func(self) -> float:
        """Calculates quadratic In easing."""
        t: float = self.current / self.duration
        return t * t


class QuadEaseOut(EasingBase):
    """Performs quadratic ease-out interpolation."""

    def func(self) -> float:
        """Calculates quadratic Out easing."""
        t: float = self.current / self.duration
        return -(t * (t - 2))


class CubicEaseIn(EasingBase):
    """Performs cubic ease-in interpolation."""

    def func(self) -> float:
        """Calculates cubic In easing."""
        t: float = self.current / self.duration
        return t * t * t


class CubicEaseOut(EasingBase):
    """Performs cubic ease-out interpolation."""

    def func(self) -> float:
        """Calculates cubic Out easing."""
        t: float = self.current / self.duration
        return (t - 1) * (t - 1) * (t - 1) + 1


class CubicEaseInOut(EasingBase):
    """Performs cubic ease-in-out interpolation."""

    def func(self) -> float:
        """Calculates cubic In-Out easing."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 4 * t * t * t
        p: float = 2 * t - 2
        return 0.5 * p * p * p + 1


class QuarticEaseIn(EasingBase):
    """Performs quartic ease-in interpolation."""

    def func(self) -> float:
        """Calculates quartic In easing."""
        t: float = self.current / self.duration
        return t * t * t * t


class QuarticEaseOut(EasingBase):
    """Performs quartic ease-out interpolation."""

    def func(self) -> float:
        """Calculates quartic Out easing."""
        t: float = self.current / self.duration
        return (t - 1) * (t - 1) * (t - 1) * (1 - t) + 1


class QuarticEaseInOut(EasingBase):
    """Performs quartic ease-in-out interpolation."""

    def func(self) -> float:
        """Calculates quartic In-Out easing."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 8 * t * t * t * t
        p: float = t - 1
        return -8 * p * p * p * p + 1


class QuinticEaseIn(EasingBase):
    """Performs quintic ease-in interpolation."""

    def func(self) -> float:
        """Calculates quintic In easing."""
        t: float = self.current / self.duration
        return t * t * t * t * t


class QuinticEaseOut(EasingBase):
    """Performs quintic ease-out interpolation."""

    def func(self) -> float:
        """Calculates quintic Out easing."""
        t: float = self.current / self.duration
        return (t - 1) * (t - 1) * (t - 1) * (t - 1) * (t - 1) + 1


class QuinticEaseInOut(EasingBase):
    """Performs quintic ease-in-out interpolation."""

    def func(self) -> float:
        """Calculates quintic In-Out easing."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 16 * t * t * t * t * t
        p: float = (2 * t) - 2
        return 0.5 * p * p * p * p * p + 1


class SineEaseIn(EasingBase):
    """Performs sine-based ease-in interpolation."""

    def func(self) -> float:
        """Calculates sine In easing."""
        t: float = self.current / self.duration
        return math.sin((t - 1) * math.pi / 2) + 1


class SineEaseOut(EasingBase):
    """Performs sine-based ease-out interpolation."""

    def func(self) -> float:
        """Calculates sine Out easing."""
        t: float = self.current / self.duration
        return math.sin(t * math.pi / 2)


class SineEaseInOut(EasingBase):
    """Performs sine-based ease-in-out interpolation."""

    def func(self) -> float:
        """Calculates sine In-Out easing."""
        t: float = self.current / self.duration
        return 0.5 * (1 - math.cos(t * math.pi))


class CircularEaseIn(EasingBase):
    """Performs circular ease-in interpolation."""

    def func(self) -> float:
        """Calculates circular In easing."""
        t: float = self.current / self.duration
        return 1 - math.sqrt(1 - (t * t))


class CircularEaseOut(EasingBase):
    """Performs circular ease-out interpolation."""

    def func(self) -> float:
        """Calculates circular Out easing."""
        t: float = self.current / self.duration
        return math.sqrt((2 - t) * t)


class CircularEaseInOut(EasingBase):
    """Performs circular ease-in-out interpolation."""

    def func(self) -> float:
        """Calculates circular In-Out easing."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 0.5 * (1 - math.sqrt(1 - 4 * (t * t)))
        return 0.5 * (math.sqrt(-((2 * t) - 3) * ((2 * t) - 1)) + 1)


class ExponentialEaseIn(EasingBase):
    """Performs exponential ease-in interpolation."""

    def func(self) -> float:
        """Calculates exponential In easing."""
        t: float = self.current / self.duration
        if t == 0:
            return 0
        return math.pow(2, 10 * (t - 1))


class ExponentialEaseOut(EasingBase):
    """Performs exponential ease-out interpolation."""

    def func(self) -> float:
        """Calculates exponential Out easing."""
        t: float = self.current / self.duration
        if t == 1:
            return 1
        return 1 - math.pow(2, -10 * t)


class ExponentialEaseInOut(EasingBase):
    """Performs exponential ease-in-out interpolation."""

    def func(self) -> float:
        """Calculates exponential In-Out easing."""
        t: float = self.current / self.duration
        if t == 0 or t == 1:
            return t
        if t < 0.5:
            return 0.5 * math.pow(2, (20 * t) - 10)
        return -0.5 * math.pow(2, (-20 * t) + 10) + 1


class ElasticEaseIn(EasingBase):
    """Performs elastic ease-in interpolation."""

    def func(self) -> float:
        """Calculates elastic In easing."""
        t: float = self.current / self.duration
        return math.sin(13 * math.pi / 2 * t) * math.pow(2, 10 * (t - 1))


class ElasticEaseOut(EasingBase):
    """Performs elastic ease-out interpolation."""

    def func(self) -> float:
        """Calculates elastic Out easing."""
        t: float = self.current / self.duration
        return math.sin(-13 * math.pi / 2 * (t + 1)) * math.pow(2, -10 * t) + 1


class ElasticEaseInOut(EasingBase):
    """Performs elastic ease-in-out interpolation."""

    def func(self) -> float:
        """Calculates elastic In-Out easing."""
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
    """Performs back-in easing, with a slight overshoot at the beginning."""

    def func(self) -> float:
        """Calculates back In easing."""
        t: float = self.current / self.duration
        return t * t * t - t * math.sin(t * math.pi)


class BackEaseOut(EasingBase):
    """Performs back-out easing, with a slight overshoot at the end."""

    def func(self) -> float:
        """Calculates back Out easing."""
        t: float = self.current / self.duration
        p: float = 1 - t
        return 1 - (p * p * p - p * math.sin(p * math.pi))


class BackEaseInOut(EasingBase):
    """Performs back-in-out easing with overshoots at both ends."""

    def func(self) -> float:
        """Calculates back In-Out easing."""
        t: float = self.current / self.duration
        if t < 0.5:
            p: float = 2 * t
            return 0.5 * (p * p * p - p * math.sin(p * math.pi))
        p: float = 1 - (2 * t - 1)
        return 0.5 * (1 - (p * p * p - p * math.sin(p * math.pi))) + 0.5


class BounceEaseIn(EasingBase):
    """Performs bounce-in easing."""

    def func(self) -> float:
        """Calculates bounce In easing by delegating to BounceEaseOut."""
        t: float = self.current / self.duration
        n: BounceEaseOut = BounceEaseOut()
        n.current = 1 - t
        n.duration = 1
        return 1 - n.func()


class BounceEaseOut(EasingBase):
    """Performs bounce-out easing."""

    def func(self) -> float:
        """Calculates bounce Out easing using piecewise functions."""
        t: float = self.current / self.duration
        if t < 4 / 11:
            return 121 * t * t / 16
        elif t < 8 / 11:
            return (363 / 40.0 * t * t) - (99 / 10.0 * t) + 17 / 5.0
        elif t < 9 / 10:
            return (4356 / 361.0 * t * t) - (35442 / 1805.0 * t) + 16061 / 1805.0
        return (54 / 5.0 * t * t) - (513 / 25.0 * t) + 268 / 25.0


class BounceEaseInOut(EasingBase):
    """Performs bounce-in-out easing."""

    def func(self) -> float:
        """Calculates bounce In-Out easing."""
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
