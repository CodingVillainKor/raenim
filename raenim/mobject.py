from manim import *
from typing import Union
from cv2 import imread, resize
from pathlib import Path

MOUSE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 100, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 249, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 244, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 240, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 240, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 240, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 240, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 230, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 230, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 240, 200, 10, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 253, 250, 10, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 237, 200, 10, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 250, 200, 10, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 240, 200, 10, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 252, 240, 200, 10, 0, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 240, 200, 10, 0, 0],
    [1, 140, 255, 255, 255, 255, 255, 255, 255, 255, 255, 161, 118, 149, 164, 182, 197, 214, 227, 242, 247, 255, 255, 10, 0],
    [1, 140, 255, 255, 255, 255, 255, 140, 165, 222, 255, 174, 1, 1, 1, 1, 3, 17, 26, 34, 59, 59, 40, 10, 0],
    [1, 140, 255, 255, 255, 255, 140, 50, 1, 144, 255, 254, 59, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 255, 140, 60, 0, 0, 56, 253, 255, 161, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 255, 140, 50, 0, 0, 0, 2, 193, 255, 241, 34, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 255, 140, 40, 0, 0, 0, 0, 0, 20, 255, 255, 129, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 140, 140, 32, 0, 0, 0, 0, 0, 0, 21, 232, 255, 223, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 140, 75, 0, 0, 0, 0, 0, 0, 0, 0, 20, 255, 255, 99, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 252, 255, 199, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 193, 255, 255, 69, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 255, 255, 174, 40, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21, 231, 255, 247, 46, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 147, 255, 255, 30, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 56, 253, 255, 248, 43, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 197, 255, 208, 50, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 56, 50, 50, 50, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


class Mouse(ImageMobject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def on(self, target):
        self.move_to(target)
        self.shift(RIGHT*0.1 + DOWN*0.2)


_surround_buf = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER

class SurroundingRect(Rectangle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def surround(self, mobject, buff_h=_surround_buf, buff_w=_surround_buf):
        self.move_to(mobject)\
            .stretch_to_fit_height(mobject.height + buff_h)\
            .stretch_to_fit_width(mobject.width + buff_w)
        return self
    
class Chainer(VGroup):
    _chain_class = {
        "plain": Line,
        "dashedline": DashedLine,
        "arrow": Arrow
    }
    def __init__(self, *args, chain_type="plain", chain_kwargs={"buff":0}, **kwargs):
        super().__init__(**kwargs)
        if len(args) <= 1:
            raise ValueError("The number of args should be larger than one.")
        
        line_cls = self._chain_class.get(chain_type, "plain")
        for now_, next_ in zip(args[:-1], args[1:]):
            self.add(line_cls(now_, next_, **chain_kwargs))

class Joiner(VGroup):
    def __init__(self, *args, join: callable, **kwargs):
        self.join = join
        super().__init__(*args, **kwargs)
    
    def add(self, *args):
        for arg in args:
            if isinstance(arg, Mobject):
                if len(self.items) > 0:
                    super().add(self.join())
                super().add(arg)
            else:
                raise ValueError("Only Mobject can be added.")
        return self
    
    @property
    def items(self):
        return [item for item in self]

class BrokenLine(TipableVMobject):
    def __init__(self, *pos, arrow=False, smooth=False, **kwargs):
        assert not (arrow and smooth), \
            "A broken line cannot be both arrowed and smooth."
        assert len(pos) > 2, \
            "A broken line must have at least three points."
        super().__init__()
        if smooth:
            self.set_points_smoothly(pos)
        else:
            self.set_points_as_corners(pos)

        if arrow:
            self.add_tip(**kwargs)


class Pixel(Square):
    def __init__(self, side_length, **kwargs):
        kwargs["stroke_width"] = kwargs.get("stroke_width", 0)
        kwargs["stroke_color"] = kwargs.get("stroke_color", GREY_D)
        kwargs["fill_opacity"] = kwargs.get("fill_opacity", 1)
        kwargs["fill_color"] = kwargs.get("fill_color", BLACK)
        super().__init__(side_length, **kwargs)

class PixelImage(VGroup):
    def __init__(
            self,
            input_: Union[str, np.ndarray], 
            pixel_size: Union[float, int, None] = None,
            *,
            pixel_kwargs={},
            img_kwargs=dict(buff=0.0)
        ):
        super().__init__()
        if isinstance(input_, str):
            input_ = Path(input_)
            if str(input_).startswith("~"):
                input_ = input_.expanduser()
            input_array = imread(input_)
        elif isinstance(input_, np.ndarray):
            input_array = input_
        else:
            raise ValueError("input_ should be a path or an array.")

        h, w = input_array.shape[:2]

        if max(h, w) > 480:
            print(
                "Warning: The input image is too large."
                "It will be resized to fit in 480 pixels."
            )
            scale = 480 / max(h, w)
            input_array = resize(input_array, (int(w * scale), int(h * scale)))

        if pixel_size is None:
            pixel_size = 3 / max(h, w)

        for i in range(input_array.shape[0]):
            for j in range(input_array.shape[1]):
                color_np = input_array[i, j]
                if np.issubdtype(color_np.dtype, np.integer):
                    if color_np.ndim == 0:
                        color_np = (int(color_np),) * 3
                    color_np = tuple(int(x) for x in color_np)
                elif np.issubdtype(color_np.dtype, np.floating):
                    if color_np.ndim == 0:
                        color_np = (float(color_np[0]),) * 3
                    color_np = tuple(float(x) for x in color_np)
                color = ManimColor(color_np)
                self.add(Pixel(pixel_size, fill_color=color, **pixel_kwargs))
        self.arrange_in_grid(h, w, **img_kwargs)

cat_path = Path(__file__).parents[1] / "vecatable.jpg"
CAT = ImageMobject(cat_path)