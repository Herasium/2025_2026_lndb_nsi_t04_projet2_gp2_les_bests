
"""
 This file includes code from the easing-functions library, originally written by
 Filippos Christianos (@semitable) and Steve C (@diceroll123).
 
 The easing-functions library is licensed under the GNU General Public License version 3.
 For more information, see the LICENSE file in the easing-functions directory or visit
 https://github.com/semitable/easing-functions.
"""

import math

class EasingBase:

    def __init__(self, start=0, end=1, duration=100):
        self.start = start
        self.end = end
        self.duration = duration
        self.current = 0

    def func(self):
        raise NotImplementedError

    def tick(self):
        if self.current < self.duration:
            value = self.func()
            self.current += 1
            return self.start + (self.end - self.start) * value
        else:
            return self.end

    def reset(self):
        self.current = 0

"""
Linear
"""
class LinearInOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return t

"""
Quadratic easing functions
"""


class QuadEaseInOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        if t < 0.5:
            return 2 * t * t
        return (-2 * t * t) + (4 * t) - 1


class QuadEaseIn(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return t * t


class QuadEaseOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return -(t * (t - 2))


"""
Cubic easing functions
"""


class CubicEaseIn(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return t * t * t


class CubicEaseOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return (t - 1) * (t - 1) * (t - 1) + 1


class CubicEaseInOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        if t < 0.5:
            return 4 * t * t * t
        p = 2 * t - 2
        return 0.5 * p * p * p + 1


"""
Quartic easing functions
"""


class QuarticEaseIn(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return t * t * t * t


class QuarticEaseOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return (t - 1) * (t - 1) * (t - 1) * (1 - t) + 1


class QuarticEaseInOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        if t < 0.5:
            return 8 * t * t * t * t
        p = t - 1
        return -8 * p * p * p * p + 1


"""
Quintic easing functions
"""


class QuinticEaseIn(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return t * t * t * t * t


class QuinticEaseOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return (t - 1) * (t - 1) * (t - 1) * (t - 1) * (t - 1) + 1


class QuinticEaseInOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        if t < 0.5:
            return 16 * t * t * t * t * t
        p = (2 * t) - 2
        return 0.5 * p * p * p * p * p + 1


"""
Sine easing functions
"""


class SineEaseIn(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return math.sin((t - 1) * math.pi / 2) + 1


class SineEaseOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return math.sin(t * math.pi / 2)


class SineEaseInOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return 0.5 * (1 - math.cos(t * math.pi))


"""
Circular easing functions
"""


class CircularEaseIn(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return 1 - math.sqrt(1 - (t * t))


class CircularEaseOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return math.sqrt((2 - t) * t)


class CircularEaseInOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        if t < 0.5:
            return 0.5 * (1 - math.sqrt(1 - 4 * (t * t)))
        return 0.5 * (math.sqrt(-((2 * t) - 3) * ((2 * t) - 1)) + 1)


"""
Exponential easing functions
"""


class ExponentialEaseIn(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        if t == 0:
            return 0
        return math.pow(2, 10 * (t - 1))


class ExponentialEaseOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        if t == 1:
            return 1
        return 1 - math.pow(2, -10 * t)


class ExponentialEaseInOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
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
        t = self.current / self.duration
        return math.sin(13 * math.pi / 2 * t) * math.pow(2, 10 * (t - 1))


class ElasticEaseOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        return math.sin(-13 * math.pi / 2 * (t + 1)) * math.pow(2, -10 * t) + 1


class ElasticEaseInOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
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
        t = self.current / self.duration
        return t * t * t - t * math.sin(t * math.pi)


class BackEaseOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        p = 1 - t
        return 1 - (p * p * p - p * math.sin(p * math.pi))


class BackEaseInOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        if t < 0.5:
            p = 2 * t
            return 0.5 * (p * p * p - p * math.sin(p * math.pi))

        p = 1 - (2 * t - 1)

        return 0.5 * (1 - (p * p * p - p * math.sin(p * math.pi))) + 0.5


"""
Bounce Easing Functions
"""


class BounceEaseIn(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        n = BounceEaseOut()
        n.current = 1 - t
        n.duration = 1
        return 1 - n.func()


class BounceEaseOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        if t < 4 / 11:
            return 121 * t * t / 16
        elif t < 8 / 11:
            return (363 / 40.0 * t * t) - (99 / 10.0 * t) + 17 / 5.0
        elif t < 9 / 10:
            return (4356 / 361.0 * t * t) - (35442 / 1805.0 * t) + 16061 / 1805.0
        return (54 / 5.0 * t * t) - (513 / 25.0 * t) + 268 / 25.0


class BounceEaseInOut(EasingBase):
    def func(self) -> float:
        t = self.current / self.duration
        if t < 0.5:
            n = BounceEaseIn()
            n.current = t * 2
            n.duration = 1
            return 0.5 * n.func()
        n = BounceEaseOut()
        n.current = t * 2 - 1
        n.duration = 1
        return 0.5 * n.func() + 0.5
    



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    # Assuming all easing functions are defined in the provided code

    def plot_easing_functions():
        easing_functions = [
            LinearInOut,
            QuadEaseIn, QuadEaseOut, QuadEaseInOut,
            CubicEaseIn, CubicEaseOut, CubicEaseInOut,
            QuarticEaseIn, QuarticEaseOut, QuarticEaseInOut,
            QuinticEaseIn, QuinticEaseOut, QuinticEaseInOut,
            SineEaseIn, SineEaseOut, SineEaseInOut,
            CircularEaseIn, CircularEaseOut, CircularEaseInOut,
            ExponentialEaseIn, ExponentialEaseOut, ExponentialEaseInOut,
            ElasticEaseIn, ElasticEaseOut, ElasticEaseInOut,
            BackEaseIn, BackEaseOut, BackEaseInOut,
            BounceEaseIn, BounceEaseOut, BounceEaseInOut,
        ]

        fig, axs = plt.subplots(len(easing_functions), 1, figsize=(10, 20))

        for i, EasingClass in enumerate(easing_functions):
            easing = EasingClass(duration=100)
            values = [easing.tick() / easing.end for _ in range(101)] # Normalize values to [0,1]

            axs[i].plot(values)
            axs[i].set_title(EasingClass.__name__)
            axs[i].set_ylim([0, 1]) # Set y-axis limits to [0,1]

        plt.tight_layout()
        plt.savefig('easing_functions.png', dpi=300, bbox_inches='tight')
        plt.close()

    plot_easing_functions()
