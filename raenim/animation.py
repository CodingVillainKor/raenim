from manim import *
from manim.mobject.mobject import _AnimationBuilder

class SkewedAnimations(list):
    def __init__(self, *animations, **kwargs):
        super().__init__()
        num_anims = len(animations)
        skewed_anims = [[None]*i for i in range(num_anims)]
            
        for anims in zip(*animations):
            for i, anim in enumerate(anims):
                skewed_anims[i].append(anim)
        
        for i in range(num_anims):
            skewed_anims[i].extend([None]*(num_anims-i-1))
        
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



if __name__ == "__main__":
    c, r, t = Circle(), Rectangle(), Text("Hello")
    VGroup(c, r, t).arrange(DOWN).shift(LEFT*4)
    num_repeat = 5
    cs = [c.animate.shift(RIGHT) for _ in range(num_repeat)]
    rs = [r.animate.shift(RIGHT) for _ in range(num_repeat)]
    ts = [t.animate.shift(RIGHT) for _ in range(num_repeat)]
    skewed_anims = SkewedAnimations(cs, rs, ts)
    breakpoint()