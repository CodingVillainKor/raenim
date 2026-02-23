from __future__ import annotations
from typing import Any, Sequence
from manim import *


_SENTINEL = object()


class RaenimPlane(NumberPlane):
    def __init__(
        self,
        # NumberPlane
        x_range: Sequence[float] | None = (-5, 5, 1),
        y_range: Sequence[float] | None = (-4, 4, 1),
        x_length: float | None = None,
        y_length: float | None = None,
        background_line_style: dict[str, Any] | None = _SENTINEL,
        faded_line_style: dict[str, Any] | None = _SENTINEL,
        faded_line_ratio: int = 1,
        make_smooth_after_applying_functions: bool = True,
        # Axes
        axis_config: dict | None = _SENTINEL,
        x_axis_config: dict | None = None,
        y_axis_config: dict | None = None,
        tips: bool = True,
        **kwargs,
    ):
        if axis_config is _SENTINEL:
            axis_config = {"stroke_color": GREY_B}
        if background_line_style is _SENTINEL:
            background_line_style = {
                "stroke_color": BLUE_D,
                "stroke_width": 2,
                "stroke_opacity": 0,
            }
        if faded_line_style is _SENTINEL:
            faded_line_style = {"stroke_opacity": 0}
        super().__init__(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            background_line_style=background_line_style,
            faded_line_style=faded_line_style,
            faded_line_ratio=faded_line_ratio,
            make_smooth_after_applying_functions=make_smooth_after_applying_functions,
            axis_config=axis_config,
            x_axis_config=x_axis_config,
            y_axis_config=y_axis_config,
            tips=tips,
            **kwargs,
        )
        self.scale(0.6)

    def markc(self, x, y, tick=True, line=True):
        """(x, y) 좌표를 표시: tick, DashedLine, Dot (updater 포함).

        Returns:
            VGroup with .dot attribute and .remove_updaters() method.
        """
        plane = self
        point = self.c2p(x, y)
        result = VGroup()
        _updaters: list[tuple[Mobject, callable]] = []

        dot = Dot(point, color=BLUE)

        if tick:
            x_tick = self.x_axis.get_tick(x, size=0.05).set_color(GREY_B)
            y_tick = self.y_axis.get_tick(y, size=0.05).set_color(GREY_B)

            def _upd_x_tick(mob, _p=plane, _d=dot):
                cx, _ = _p.p2c(_d.get_center())
                mob.become(_p.x_axis.get_tick(cx, size=0.05).set_color(GREY_B))

            def _upd_y_tick(mob, _p=plane, _d=dot):
                _, cy = _p.p2c(_d.get_center())
                mob.become(_p.y_axis.get_tick(cy, size=0.05).set_color(GREY_B))

            x_tick.add_updater(_upd_x_tick)
            y_tick.add_updater(_upd_y_tick)
            _updaters.append((x_tick, _upd_x_tick))
            _updaters.append((y_tick, _upd_y_tick))
            result.add(x_tick, y_tick)

        if line:
            h_line = DashedLine(
                self.c2p(0, y), point,
                dash_length=0.1, dashed_ratio=0.7,
                color=GREY_C, stroke_width=3,
            )
            v_line = DashedLine(
                self.c2p(x, 0), point,
                dash_length=0.1, dashed_ratio=0.7,
                color=GREY_C, stroke_width=3,
            )

            def _upd_h_line(mob, _p=plane, _d=dot):
                cx, cy = _p.p2c(_d.get_center())
                mob.become(DashedLine(
                    _p.c2p(0, cy), _p.c2p(cx, cy),
                    dash_length=0.1, dashed_ratio=0.7,
                    color=GREY_C, stroke_width=3,
                ))

            def _upd_v_line(mob, _p=plane, _d=dot):
                cx, cy = _p.p2c(_d.get_center())
                mob.become(DashedLine(
                    _p.c2p(cx, 0), _p.c2p(cx, cy),
                    dash_length=0.1, dashed_ratio=0.7,
                    color=GREY_C, stroke_width=3,
                ))

            h_line.add_updater(_upd_h_line)
            v_line.add_updater(_upd_v_line)
            _updaters.append((h_line, _upd_h_line))
            _updaters.append((v_line, _upd_v_line))
            result.add(h_line, v_line)

        result.add(dot)
        result.dot = dot

        def _remove_updaters():
            for mob, fn in _updaters:
                mob.remove_updater(fn)

        result.remove_updaters = _remove_updaters
        return result


class RaenimLine(NumberLine):
    def __init__(self, **kwargs):
        # ── NumberLine 고유 ──
        # x_range=None,                      # (min, max, step), 기본 [-7, 7, 1]
        # length=None,                       # 설정하면 unit_size 무시
        # unit_size=1,

        # ── 틱 ──
        # include_ticks=True,
        # tick_size=0.1,
        # numbers_with_elongated_ticks=None,
        # longer_tick_multiple=2,
        # exclude_origin_tick=False,

        # ── 팁 (화살표) ──
        # include_tip=False,
        # tip_width=0.35,
        # tip_height=0.35,
        # tip_shape=None,

        # ── 숫자 라벨 ──
        # include_numbers=False,
        # font_size=36,
        # label_direction=DOWN,
        # label_constructor=MathTex,
        # scaling=LinearBase(),
        # line_to_number_buff=MED_SMALL_BUFF,  # 0.25
        # decimal_number_config=None,
        # numbers_to_exclude=None,
        # numbers_to_include=None,

        # ── 외형 ──
        # rotation=0,                        # 라디안
        # stroke_width=2.0,
        # stroke_color=None,
        # stroke_opacity=1.0,
        # color=WHITE,

        # ── Line / VMobject ──
        # buff=0,
        # path_arc=0,
        # fill_color=None,
        # fill_opacity=0.0,
        # background_stroke_color=BLACK,
        # background_stroke_width=0,
        # sheen_factor=0.0,
        # z_index=0,

        super().__init__(**kwargs)
