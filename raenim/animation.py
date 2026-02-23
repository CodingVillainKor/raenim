from random import random
from manim import *
from manim.mobject.mobject import _AnimationBuilder
from noise import pnoise1


class SkewedAnimations(list):
    def __init__(self, *animations, **kwargs):
        super().__init__()
        num_anims = len(animations)
        skewed_anims = [[None] * i for i in range(num_anims)]

        for anims in zip(*animations):
            for i, anim in enumerate(anims):
                skewed_anims[i].append(anim)

        for i in range(num_anims):
            skewed_anims[i].extend([None] * (num_anims - i - 1))

        for anims in zip(*skewed_anims):
            anim = []
            for a in anims:
                if a is not None:
                    anim.append(a)
            self.append(anim)

    def __getitem__(self, i):
        item = super().__getitem__(i)
        return self.override_to_current_animate(item)

    def __iter__(self):
        for item in super().__iter__():
            for i in range(len(item)):
                item[i] = self.override_to_current_animate(item[i])
            yield item

    @staticmethod
    def override_to_current_animate(anim):
        if isinstance(anim, _AnimationBuilder):
            m_names = anim.method_names
            args = [m[1] for m in anim.methods]
            kwargs = [m[2] for m in anim.methods]
            anim = anim.mobject.animate
            for m_name, args, kwargs in zip(m_names, args, kwargs):
                anim = getattr(anim, m_name)(*args, **kwargs)
            return anim
        else:
            return anim


def AnchorToPoint(
    group: VGroup, dest: VMobject | np.ndarray, anchor: VMobject | np.ndarray
):
    if isinstance(anchor, VMobject):
        anchor = anchor.get_center()
    if isinstance(dest, VMobject):
        dest = dest.get_center()
    shift = dest - anchor
    return group.animate.shift(shift)


import numpy as np
from noise import pnoise1  # manim에서 잘 동작함


def wiggle_shift(
    t,
    amp=(0.1, 0.1, 0.0),
    freq=0.5,
    phase=(0.0, 20.0, 40.0),
):
    """
    t     : time (float)
    amp   : (Ax, Ay, Az)
    freq  : wiggle frequency
    phase : axis-wise phase offsets
    """

    dx = amp[0] * pnoise1(freq * t + phase[0])
    dy = amp[1] * pnoise1(freq * t + phase[1])
    dz = amp[2] * pnoise1(freq * t + phase[2])
    return np.array([dx, dy, dz])


class RWiggle(Animation):
    """
    Animation that makes a mobject wiggle randomly using Perlin noise.
    Smoothly returns to the original position at the end using interpolation.

    Parameters
    ----------
    mobject : Mobject
        The object to wiggle
    amp : tuple
        Amplitude tuple (x, y, z) for wiggle strength
    speed : float
        Frequency/speed of the wiggle
    phase : tuple
        Phase offset tuple (x, y, z) for independent axis movement.
        If None, random phase offsets will be generated.
    run_time : float
        Duration of the animation

    Examples
    --------
    self.play(RWiggle(obj))
    self.play(RWiggle(obj, amp=(0.2, 0.2, 0.0), speed=1.0))
    """

    def __init__(
        self,
        mobject: Mobject,
        amp: tuple | float | None = None,
        speed: float | None = None,
        phase=None,
        pow=8,
        run_time=2.0,
        **kwargs,
    ):
        if amp is None:
            amp = (0.1, 0.1, 0.1)
        elif isinstance(amp, (int, float)):
            amp = (amp, amp, amp)
        
        if speed is None:
            speed = amp[0] * 40

        self.amp = amp
        self.freq = speed
        self.phase = (
            phase
            if phase is not None
            else (random() * 30 - 15, random() * 30 - 15, random() * 30 - 15)
        )
        self.initial_position = None
        self.initial_wiggle_offset = None  # Store t=0 wiggle value
        self.pow = pow
        super().__init__(mobject, run_time=run_time, **kwargs)

    def begin(self):
        """Store the initial position and wiggle offset when animation starts"""
        self.initial_position = self.mobject.get_center().copy()
        # Store wiggle value at t=0 to ensure smooth start from displacement=0
        self.initial_wiggle_offset = wiggle_shift(0, self.amp, self.freq, self.phase)
        super().begin()

    def wiggle_fn(self, alpha: float, pow: float = 8):
        """
        Calculate wiggle displacement based on animation progress.
        Uses interpolation with (1 - alpha^pow) to smoothly return to origin.

        Parameters
        ----------
        alpha : float
            Animation progress (0 = start, 1 = end)
        """
        from manim.utils.bezier import interpolate

        t = alpha * self.run_time
        # Subtract initial offset to ensure displacement starts at [0,0,0]
        wiggle_displacement = wiggle_shift(t, self.amp, self.freq, self.phase) - self.initial_wiggle_offset

        # Interpolate between wiggle and zero displacement
        # At alpha=0: factor=1 (full wiggle, but displacement=0 due to offset)
        # At alpha=1: factor=0 (no wiggle, returns to initial position)
        fade_factor = 1 - alpha**pow
        displacement = interpolate(np.zeros(3), wiggle_displacement, fade_factor)

        return displacement

    def interpolate_mobject(self, alpha: float):
        """Update mobject position each frame"""
        displacement = self.wiggle_fn(alpha, pow=self.pow)
        new_position = self.initial_position + displacement
        self.mobject.move_to(new_position)


def anticipation_rate(a=0.12, t0=0.18, ease1=smooth, ease2=rush_from):
    """
    Create a rate function with anticipation effect.

    a  : anticipation amount (0.05~0.25 recommended)
    t0 : anticipation duration ratio (0.1~0.3 recommended)
    ease1: easing function for anticipation phase
    ease2: easing function for main movement phase
    """
    def rf(t):
        if t < t0:
            u = t / t0
            return -a * ease1(u)                 # 0 -> -a
        else:
            u = (t - t0) / (1 - t0)
            return -a + (1 + a) * ease2(u)       # -a -> 1
    return rf


class AMove(Transform):
    """
    Animation that moves a mobject with anticipation before moving to the target position.

    Uses anticipation_rate function for smooth motion without discontinuities.

    Parameters
    ----------
    mobject : Mobject
        The object to move
    target_point : np.ndarray | Mobject
        The target position to move to (can be a point or mobject)
    anticipation_amount : float
        How far to move backward (0.05~0.25 recommended). Default 0.12
    anticipation_ratio : float
        Time ratio for anticipation phase (0.1~0.3 recommended). Default 0.18
    ease1 : callable
        Easing function for anticipation phase. Default is smooth
    ease2 : callable
        Easing function for main movement phase. Default is smooth
    run_time : float
        Duration of the animation

    Examples
    --------
    self.play(AMove(obj, target_point=RIGHT * 3))
    self.play(AMove(obj, target_point=UP * 2, anticipation_amount=0.15))
    """
    def __init__(
        self,
        mobject: Mobject,
        target_point: np.ndarray | Mobject,
        anticipation_amount: float = 0.1,
        anticipation_ratio: float = 0.4,
        run_time: float = 1.5,
        **kwargs,
    ):
        # Create target mobject at the target position
        if isinstance(target_point, Mobject):
            target_point = target_point.get_center()

        target_mobject = mobject.copy()
        target_mobject.move_to(target_point)

        # Set up rate function
        rate_func = anticipation_rate(
            a=anticipation_amount,
            t0=anticipation_ratio,
        )

        super().__init__(
            mobject,
            target_mobject,
            rate_func=rate_func,
            run_time=run_time,
            **kwargs
        )

class Transformr(Transform):
    def __init__(
        self,
        mobject: Mobject,
        target_mobject: Mobject,
        **kwargs,
    ):
        super().__init__(
            mobject,
            target_mobject,
            replace_mobject_with_target_in_scene=True,
            **kwargs
    )