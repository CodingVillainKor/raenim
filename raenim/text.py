from manim import *
from .utils import MONO_FONT

__all__ = ["CodeText", "ListText", "TextBox", "TexBox", "Words", "RaeTex"]

class CodeText(Text):
    def __init__(self, text, **kwargs):
        kwargs["font_size"] = kwargs.pop("font_size", 24)
        kwargs["font"] = kwargs.pop("font", MONO_FONT)
        super().__init__(text, **kwargs)

class ListText(VGroup):
    def __init__(self, *texts, font_size=48, color=WHITE, arrange=RIGHT, no_bracket=False, **kwargs):
        super().__init__()
        t = VGroup(*[text if isinstance(text, Mobject) else Text(str(text), font_size=font_size, color=color, **kwargs) for text in texts]).arrange(arrange)
        if no_bracket:
            self.add(*t)
            return
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

class Words(Text):
    def __init__(self, text:str, **kwargs):
        super().__init__(text, **kwargs)
        words_idx = self._build_spans(text)
        self.words = VGroup(*[self[i:j] for i, j in words_idx])

    @staticmethod
    def _build_spans(s: str) -> list[tuple[int, int]]:
        spans: list[tuple[int, int]] = []
        in_word = False
        nonws_idx = 0
        start_nonws = 0

        for ch in s:
            if ch.isspace():
                if in_word:
                    spans.append((start_nonws, nonws_idx))
                    in_word = False
            else:
                if not in_word:
                    start_nonws = nonws_idx
                    in_word = True
                nonws_idx += 1

        if in_word:
            spans.append((start_nonws, nonws_idx))

        return spans
    
class RaeTex(MathTex):
    def __init__(self, *tex_strings: list[str], items=None, **kwargs):
        super().__init__(*tex_strings, substrings_to_isolate=items, **kwargs)

    def __getitem__(self, index: int | str) -> MathTex:
        if isinstance(index, (int, slice)):
            return super().__getitem__(index)
        else:
            result = self.get_parts_by_tex(index)
            return result

    @property
    def strings(self) -> list[str]:
        return self.tex_strings
