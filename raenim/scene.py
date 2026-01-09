from manim import *
from functools import wraps
from addict import Dict

from .mobject import MOUSE, Mouse

__all__ = ["Scene2D", "Scene3D"]


class RaenimScene:
    """Base class for common functionality shared between Scene2D and Scene3D"""

    def playw(self, *args, wait=1, **kwargs):
        self.play(*args, **kwargs)
        if wait > 0:
            self.wait(wait)

    def addw(self, *args, wait=1, **kwargs):
        self.add(*args, **kwargs)
        if wait > 0:
            self.wait(wait)

    def clear(self):
        for m in self.mobjects:
            m.clear_updaters()
        self.playw(*[FadeOut(mob) for mob in self.mobjects])

    def to_front(self, *mobjects):
        self.add_foreground_mobjects(*mobjects)

    def playw_return(self, *args, **kwargs):
        self.playw(*args, rate_func=rate_functions.there_and_back, **kwargs)

    def playwl(self, *args, lag_ratio=0.05, wait=1, **kwargs):
        self.playw(LaggedStart(*args, lag_ratio=lag_ratio), wait=wait, **kwargs)

    def play_camera(self, to=ORIGIN, scale=1, **play_kwargs):
        self.playw(self.camera.frame.animate.move_to(to).scale(scale), **play_kwargs)

    def organize(self, local_vars: dict) -> Dict:
        mobjects = {k: v for k, v in local_vars.items() if isinstance(v, Mobject)}
        return Dict(mobjects)

    @property
    def mouse(self):
        if getattr(self, "_mouse", None) is None:
            self._mouse = Mouse(self._get_mouse_array())
        return self._mouse

    @staticmethod
    def _get_mouse_array():
        mouse = MOUSE.copy()
        mouse = np.array(mouse)[..., None].repeat(4, -1)
        mouse[..., -1] = (mouse[..., 0] != 0) * 255
        return mouse


class Scene2D(MovingCameraScene, RaenimScene):
    def construct(self):
        pass

    def point_mouse_to(self, point: Mobject | np.ndarray, *, from_: Mobject | np.ndarray = None, **kwargs):
        if from_ is None:
            from_ = self.mouse
        if from_ == RIGHT:
            from_ = self.cf.get_right() + from_

    @property
    def cf(self) -> VMobject:
        return self.camera.frame


class Scene3D(ThreeDScene, RaenimScene):
    def construct(self):
        pass

    def tilt_camera_horizontal(self, degree, zoom=1.0):
        phi_tilt_degree = degree * DEGREES
        theta_tilt_degree = 90 * DEGREES
        gamma_tilt_degree = -90 * DEGREES

        self.set_camera(
            phi=phi_tilt_degree,
            theta=-90 * DEGREES - theta_tilt_degree,
            gamma=gamma_tilt_degree,
            zoom=zoom,
        )

    def tilt_camera_vertical(self, degree, zoom=1.0):
        phi_tilt_degree = degree * DEGREES

        self.set_camera(
            phi=phi_tilt_degree,
            zoom=zoom,
        )

    def move_camera_horizontally(self, degree, zoom=1.0, added_anims=[], wait=1.0):
        phi_tilt_degree = degree * DEGREES
        theta_tilt_degree = 90 * DEGREES
        gamma_tilt_degree = -90 * DEGREES

        self.move_camera(
            phi=phi_tilt_degree,
            theta=-90 * DEGREES - theta_tilt_degree,
            gamma=gamma_tilt_degree,
            zoom=zoom,
            added_anims=added_anims,
        )
        self.wait(wait)

    def move_camera_vertically(self, degree, zoom=1.0, added_anims=[], wait=1.0):
        phi_tilt_degree = degree * DEGREES

        self.move_camera(phi=phi_tilt_degree, zoom=zoom, added_anims=added_anims)
        self.wait(wait)

    @wraps(ThreeDScene.set_camera_orientation)
    def set_camera(self, *args, **kwargs):
        return self.set_camera_orientation(*args, **kwargs)

    @property
    def cf(self) -> VMobject:
        return self.renderer.camera._frame_center
