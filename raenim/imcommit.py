from manim import *
from manim.utils.space_ops import angle_of_vector, normalize


class Logo(VGroup):
    def __init__(self, size=0.4, stroke_width=0.1, fill_color=BLACK, **kwargs):
        super().__init__(**kwargs)
        rdiff_line_ratio = 120
        line_length_ratio = 1
        outer_circle = Circle(
            radius=size, color=WHITE, fill_opacity=1, stroke_width=0
        ).set_z_index(0)
        inner_circle = Circle(
            radius=size - stroke_width, color=fill_color, fill_opacity=1, stroke_width=0
        ).set_z_index(0.1)
        line1 = Line(
            outer_circle.get_bottom() + DOWN * size * line_length_ratio,
            outer_circle.get_bottom(),
            color=WHITE,
            stroke_width=stroke_width * rdiff_line_ratio,
        )
        line2 = Line(
            outer_circle.get_top(),
            outer_circle.get_top() + UP * size * line_length_ratio,
            color=WHITE,
            stroke_width=stroke_width * rdiff_line_ratio,
        )

        self.add(inner_circle, outer_circle, line1, line2)

    def line_to(self, target, *, which=1):
        angle0 = angle_of_vector(
            self[which + 1].get_end() - self[which + 1].get_start()
        )
        

        if isinstance(target, Mobject):
            target = target.get_center()
        angle = angle_of_vector(target - self[0].get_center())
        circle_pos = self[1].point_at_angle(angle)
        dest = circle_pos + normalize(circle_pos - self[1].get_center())
        self[which + 1].generate_target()
        self[which + 1].target.put_start_and_end_on(circle_pos, dest)

        return MoveToTarget(self[which + 1])


class Test(Scene):
    def construct(self):
        logo = Logo()
        rect = Rectangle(
            width=0.5,
            height=0.5,
            color=WHITE,
            fill_opacity=1,
            stroke_width=0,
        ).shift(UP * 3 + RIGHT * 2)
        self.add(logo, rect)
        self.wait()
        self.play(logo.line_to(rect, which=1))
        self.wait(2)
