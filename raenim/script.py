from manim import *

__all__ = ["PythonCode"]

class PythonCode(Code):
    def __init__(self, filename, **kwargs):
        kwargs["tab_width"] = kwargs.pop("tab_width", 4)
        kwargs["language"] = kwargs.pop("language", "python")
        kwargs.pop("background", "window")
        paragraph_config = {
            "line_spacing": kwargs.pop("line_spacing", 0.6),
            "font": kwargs.pop("font", "Noto Mono")
        }
        super().__init__(filename, paragraph_config=paragraph_config, **kwargs)
        self.frame.set_opacity(0.3)
        with open(filename, "r") as f:
            self.code_string = f.read()
        self.indentation_chars = kwargs.get("indentation_chars", "    ")

    @property
    def frame(self):
        return self[:-1]
    
    @property
    def script(self):
        return self.code_lines
    
    @property
    def code(self):
        return self.code_lines
    
    def find_text(self, line_no:int, text:str, nth:int=1):
        lines = self.code_string.split("\n")
        line = lines[line_no-1]
        try:
            idx = _find_multiple(line, text)[nth-1]
        except IndexError:
            raise IndexError(f"Cannot find {nth}th {text} at line {line_no}: {line}")
        
        indentation_level = _count_indentation(line)
        idx -= (len(self.indentation_chars)-1) * indentation_level
        return idx, idx+len(text)
    
    def text_slice(self, line_no:int, text:str, nth:int=1, exclusive=False) -> Mobject:
        idx_start, idx_end = self.find_text(line_no, text, nth)
        if exclusive:
            return VGroup(self.code[line_no-1][:idx_start], self.code[line_no-1][idx_end:])
        else:
            return self.code[line_no-1][idx_start:idx_end]
    
    def highlight(self, line_no:int, text:str=None, nth:int=1, 
                  anim=Write, color="#FFFF00", anim_out=FadeOut):
        if text is None:
            target = self.code[line_no-1].copy().set_color(color)
        else:
            target = self.text_slice(line_no, text, nth).copy().set_color(color)
        return anim(target), anim_out(target)

    def __call__(self, *line) -> VMobject:
        is_negative = lambda x: x < 0
        if len(line) == 1:
            return self.code[line[0]-1*is_negative(line[0])]
        elif len(line) == 2:
            return self.code[line[0]-1*is_negative(line[0]):line[1]]
        else:
            raise ValueError(f"The number of argument line should be 1 or 2, but {len(line)} given")


def _find_multiple(string, target):
    return [i for i in range(len(string)) if string.find(target, i) == i]

def _count_indentation(text):
    for i in range(len(text)):
        if text[i] == " ":
            continue
        else:
            return i // 4