from manim import *

__all__ = ["CodeText", "ListText"]

class CodeText(Text):
    def __init__(self, text, **kwargs):
        kwargs["font_size"] = kwargs.pop("font_size", 24)
        kwargs["font"] = kwargs.pop("font", "Consolas")
        super().__init__(text, **kwargs)

class ListText(VGroup):
    def __init__(self, *texts, font_size=48, color=WHITE, arrange=RIGHT, **kwargs):
        super().__init__(**kwargs)
        t = VGroup(*[text if isinstance(text, Mobject) else Text(str(text), font_size=font_size, color=color, **kwargs) for text in texts]).arrange(arrange)
        bracket0 = Text("[", font_size=font_size, color=color, **kwargs).next_to(t[0], LEFT)
        bracket1 = Text("]", font_size=font_size, color=color, **kwargs).next_to(t[-1], RIGHT)
        self.add(bracket0, *t, bracket1)
