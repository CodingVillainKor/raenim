from manim import *

__all__ = ["CodeText", "ListText", "TextBox", "TexBox"]

class CodeText(Text):
    def __init__(self, text, **kwargs):
        kwargs["font_size"] = kwargs.pop("font_size", 24)
        kwargs["font"] = kwargs.pop("font", "Noto Mono")
        super().__init__(text, **kwargs)

class ListText(VGroup):
    def __init__(self, *texts, font_size=48, color=WHITE, arrange=RIGHT, **kwargs):
        super().__init__(**kwargs)
        t = VGroup(*[text if isinstance(text, Mobject) else Text(str(text), font_size=font_size, color=color, **kwargs) for text in texts]).arrange(arrange)
        bracket0 = Text("[", font_size=font_size, color=color, **kwargs).next_to(t[0], LEFT)
        bracket1 = Text("]", font_size=font_size, color=color, **kwargs).next_to(t[-1], RIGHT)
        self.add(bracket0, *t, bracket1)

class TextBox(VGroup):
    _text_kwargs = {
        "font_size": 24,
        "color": WHITE
    }
    _box_kwargs = {
        "color": WHITE,
        "fill_color": BLACK,
        "fill_opacity": 0.75,
        "buff": 0.1,
        "corner_radius": 0.1
    }
    def __init__(
        self, text, text_kwargs=_text_kwargs, box_kwargs=_box_kwargs, **kwargs
    ):
        text = Text(text, **text_kwargs).set_z_index(0.1)
        box = SurroundingRectangle(text, **box_kwargs).set_z_index(0)
        self.text = text
        self.box = box
        super().__init__(text, box, **kwargs)
    
    def set_z_index(self, z_index):
        self.text.set_z_index(z_index+0.1)
        self.box.set_z_index(z_index)
        return self
    
class TexBox(VGroup):
    _text_kwargs = {
        "font_size": 24,
        "color": WHITE
    }
    _box_kwargs = {
        "color": WHITE,
        "fill_color": BLACK,
        "fill_opacity": 0.75,
        "buff": 0.1,
        "corner_radius": 0.1
    }
    def __init__(
        self, *text, tex_kwargs=_text_kwargs, box_kwargs=_box_kwargs, **kwargs
    ):
        tex = MathTex(*text, **tex_kwargs).set_z_index(0.1)
        box = SurroundingRectangle(tex, **box_kwargs).set_z_index(0)
        self.tex = tex
        self.box = box
        super().__init__(tex, box, **kwargs)
    
    def set_z_index(self, z_index):
        self.tex.set_z_index(z_index+0.1)
        self.box.set_z_index(z_index)
        return self