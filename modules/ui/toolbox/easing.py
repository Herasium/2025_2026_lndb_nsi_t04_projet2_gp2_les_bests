"""
This file includes code from the easing-functions library, originally written by
Filippos Christianos (@semitable) and Steve C (@diceroll123).

The easing-functions library is licensed under the GNU General Public License version 3.
For more information, see the LICENSE file in the easing-functions directory or visit
https://github.com/semitable/easing-functions.
"""

import math


class EasingBase:
    """Base class for all easing functions."""

    def __init__(self, start: float = 0, end: float = 1, duration: int = 100) -> None:
        """Initialize the easing object.

        Parameters:
        - start: The starting value
        - end: The ending value
        - duration: Total number of steps/ticks to complete the animation
        """
        self.start: float = start
        self.end: float = end
        self.duration: int = duration
        self.current: int = 0
        self.done: bool = False

    def func(self) -> float:
        """Calculate the normalized easing progress.
        Must be implemented by subclasses.

        Returns:
        - float: The progress value between 0.0 and 1.0
        """
        raise NotImplementedError

    def tick(self) -> float:
        """Advance the animation by one step and calculate the current value.

        Returns:
        - float: The calculated value at the current step
        """
        if self.current < self.duration:
            value: float = self.func()  # Get normalized progression from subclass
            self.current += 1  # Increment progress counter
            return self.start + (self.end - self.start) * value
        else:
            self.done = True  # Mark as finished
            return self.end  # Ensure final value is returned

    def reset(self) -> None:
        """Reset the animation state to the beginning."""
        self.current = 0
        self.done = False


"""
Linear
"""


class LinearInOut(EasingBase):
    def func(self) -> float:
        """Calculate linear easing."""
        t: float = self.current / self.duration
        return t


"""
Quadratic easing functions
"""


class QuadEaseInOut(EasingBase):
    def func(self) -> float:
        """Calculate quadratic In-Out easing."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 2 * t * t
        return (-2 * t * t) + (4 * t) - 1


class QuadEaseIn(EasingBase):
    def func(self) -> float:
        """Calculate quadratic In easing."""
        t: float = self.current / self.duration
        return t * t


class QuadEaseOut(EasingBase):
    def func(self) -> float:
        """Calculate quadratic Out easing."""
        t: float = self.current / self.duration
        return -(t * (t - 2))


"""
Cubic easing functions
"""


class CubicEaseIn(EasingBase):
    def func(self) -> float:
        """Calculate cubic In easing."""
        t: float = self.current / self.duration
        return t * t * t


class CubicEaseOut(EasingBase):
    def func(self) -> float:
        """Calculate cubic Out easing."""
        t: float = self.current / self.duration
        return (t - 1) * (t - 1) * (t - 1) + 1


class CubicEaseInOut(EasingBase):
    def func(self) -> float:
        """Calculate cubic In-Out easing."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 4 * t * t * t
        p: float = 2 * t - 2
        return 0.5 * p * p * p + 1


"""
Quartic easing functions
"""


class QuarticEaseIn(EasingBase):
    def func(self) -> float:
        """Calculate quartic In easing."""
        t: float = self.current / self.duration
        return t * t * t * t


class QuarticEaseOut(EasingBase):
    def func(self) -> float:
        """Calculate quartic Out easing."""
        t: float = self.current / self.duration
        return (t - 1) * (t - 1) * (t - 1) * (1 - t) + 1


class QuarticEaseInOut(EasingBase):
    def func(self) -> float:
        """Calculate quartic In-Out easing."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 8 * t * t * t * t
        p: float = t - 1
        return -8 * p * p * p * p + 1


"""
Quintic easing functions
"""


class QuinticEaseIn(EasingBase):
    def func(self) -> float:
        """Calculate quintic In easing."""
        t: float = self.current / self.duration
        return t * t * t * t * t


class QuinticEaseOut(EasingBase):
    def func(self) -> float:
        """Calculate quintic Out easing."""
        t: float = self.current / self.duration
        return (t - 1) * (t - 1) * (t - 1) * (t - 1) * (t - 1) + 1


class QuinticEaseInOut(EasingBase):
    def func(self) -> float:
        """Calculate quintic In-Out easing."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 16 * t * t * t * t * t
        p: float = (2 * t) - 2
        return 0.5 * p * p * p * p * p + 1


"""
Sine easing functions
"""


class SineEaseIn(EasingBase):
    def func(self) -> float:
        """Calculate sine In easing."""
        t: float = self.current / self.duration
        return math.sin((t - 1) * math.pi / 2) + 1


class SineEaseOut(EasingBase):
    def func(self) -> float:
        """Calculate sine Out easing."""
        t: float = self.current / self.duration
        return math.sin(t * math.pi / 2)


class SineEaseInOut(EasingBase):
    def func(self) -> float:
        """Calculate sine In-Out easing."""
        t: float = self.current / self.duration
        return 0.5 * (1 - math.cos(t * math.pi))


"""
Circular easing functions
"""


class CircularEaseIn(EasingBase):
    def func(self) -> float:
        """Calculate circular In easing."""
        t: float = self.current / self.duration
        return 1 - math.sqrt(1 - (t * t))


class CircularEaseOut(EasingBase):
    def func(self) -> float:
        """Calculate circular Out easing."""
        t: float = self.current / self.duration
        return math.sqrt((2 - t) * t)


class CircularEaseInOut(EasingBase):
    def func(self) -> float:
        """Calculate circular In-Out easing."""
        t: float = self.current / self.duration
        if t < 0.5:
            return 0.5 * (1 - math.sqrt(1 - 4 * (t * t)))
        return 0.5 * (math.sqrt(-((2 * t) - 3) * ((2 * t) - 1)) + 1)


"""
Exponential easing functions
"""


class ExponentialEaseIn(EasingBase):
    def func(self) -> float:
        """Calculate exponential In easing."""
        t: float = self.current / self.duration
        if t == 0:
            return 0
        return math.pow(2, 10 * (t - 1))


class ExponentialEaseOut(EasingBase):
    def func(self) -> float:
        """Calculate exponential Out easing."""
        t: float = self.current / self.duration
        if t == 1:
            return 1
        return 1 - math.pow(2, -10 * t)


class ExponentialEaseInOut(EasingBase):
    def func(self) -> float:
        """Calculate exponential In-Out easing."""
        t: float = self.current / self.duration
        if t == 0 or t == 1:
            return t

        if t < 0.5:
            return 0.5 * math.pow(2, (20 * t) - 10)
        return -0.5 * math.pow(2, (-20 * t) + 10) + 1


"""
Elastic Easing Functions
"""


class ElasticEaseIn(EasingBase):
    def func(self) -> float:
        """Calculate elastic In easing."""
        t: float = self.current / self.duration
        return math.sin(13 * math.pi / 2 * t) * math.pow(2, 10 * (t - 1))


class ElasticEaseOut(EasingBase):
    def func(self) -> float:
        """Calculate elastic Out easing."""
        t: float = self.current / self.duration
        return math.sin(-13 * math.pi / 2 * (t + 1)) * math.pow(2, -10 * t) + 1


class ElasticEaseInOut(EasingBase):
    def func(self) -> float:
        """Calculate elastic In-Out easing."""
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


"""
Back Easing Functions
"""


class BackEaseIn(EasingBase):
    def func(self) -> float:
        """Calculate back In easing."""
        t: float = self.current / self.duration
        return t * t * t - t * math.sin(t * math.pi)


class BackEaseOut(EasingBase):
    def func(self) -> float:
        """Calculate back Out easing."""
        t: float = self.current / self.duration
        p: float = 1 - t
        return 1 - (p * p * p - p * math.sin(p * math.pi))


class BackEaseInOut(EasingBase):
    def func(self) -> float:
        """Calculate back In-Out easing."""
        t: float = self.current / self.duration
        if t < 0.5:
            p: float = 2 * t
            return 0.5 * (p * p * p - p * math.sin(p * math.pi))

        p: float = 1 - (2 * t - 1)
        return 0.5 * (1 - (p * p * p - p * math.sin(p * math.pi))) + 0.5


"""
Bounce Easing Functions
"""


class BounceEaseIn(EasingBase):
    def func(self) -> float:
        """Calculate bounce In easing by delegating to BounceEaseOut."""
        t: float = self.current / self.duration
        n: BounceEaseOut = BounceEaseOut()  # Reuse logic for inversion
        n.current = 1 - t
        n.duration = 1
        return 1 - n.func()


class BounceEaseOut(EasingBase):
    def func(self) -> float:
        """Calculate bounce Out easing using piecewise functions."""
        t: float = self.current / self.duration
        if t < 4 / 11:
            return 121 * t * t / 16
        elif t < 8 / 11:
            return (363 / 40.0 * t * t) - (99 / 10.0 * t) + 17 / 5.0
        elif t < 9 / 10:
            return (4356 / 361.0 * t * t) - (35442 / 1805.0 * t) + 16061 / 1805.0
        return (54 / 5.0 * t * t) - (513 / 25.0 * t) + 268 / 25.0


class BounceEaseInOut(EasingBase):
    def func(self) -> float:
        """Calculate bounce In-Out easing."""
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
