from manim import *
from manim.utils.space_ops import angle_of_vector, normalize


class Logo(VGroup):
    def __init__(self, size=0.4, stroke_width=0.1, fill_color=BLACK, **kwargs):
        super().__init__(**kwargs)
        rdiff_line_ratio = 120
        line_length_ratio = 1
        self.outer_circle = Circle(
            radius=size, color=GREY_B, fill_opacity=1, stroke_width=0
        ).set_z_index(0)
        self.inner_circle = Circle(
            radius=size - stroke_width, color=fill_color, fill_opacity=1, stroke_width=0
        ).set_z_index(0.1)
        self.line_fn = lambda angle, length: Line(
            self.outer_circle.point_at_angle(angle),
            self.outer_circle.point_at_angle(angle)
            + normalize(
                self.outer_circle.point_at_angle(angle) - self.outer_circle.get_center()
            )
            * length,
            color=GREY_B,
            stroke_width=stroke_width * rdiff_line_ratio,
        )
        self.line1 = self.line_fn(-PI / 2, length=size * line_length_ratio)
        self.line2 = self.line_fn(PI / 2, length=size * line_length_ratio)

        self.add(self.inner_circle, self.outer_circle, self.line1, self.line2)

    def line_to(self, target, *, which=1):
        line: Line = getattr(self, f"line{which}")
        angle0 = angle_of_vector(line.get_end() - line.get_start())
        length0 = line.get_length()

        angle_value = ValueTracker(angle0)
        update_fn = lambda x: x.become(self.line_fn(angle_value.get_value(), length0))
        line.add_updater(update_fn)

        if isinstance(target, Mobject):
            target = target.get_center()
        angle = angle_of_vector(target - self[0].get_center())
        angle_value.generate_target().set_value(angle)
        return Succession(
            MoveToTarget(angle_value),
            UpdateFromFunc(line, lambda x: x.remove_updater(update_fn), run_time=0.01),
            UpdateFromFunc(line, lambda x: x.become(self.line_fn(angle_value.target.get_value(), length0)), run_time=0.01),
        )