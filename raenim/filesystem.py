from manim import *

__all__ = ["File", "Folder", "FileSystem", "FolderIcon", "FileIcon"]

class File(VGroup):
    def __init__(self, size=2):
        super().__init__()
        nump = NumberPlane()
        ratio = 16/9/1.4
        ul = (-size/2, size/2*ratio)
        ur = (size/2, size/2*ratio)
        dl = (-size/2, -size/2*ratio)
        dr = (size/2, -size/2*ratio)
        
        rect_coords = [nump.c2p(*item) for item in [ul, ur, dr, dl]]
        paper = Polygon(*rect_coords, stroke_width=3*size, color=GREY_C).set_fill(WHITE, opacity=1)
        
        cut_ratio = 0.3
        fold_top = (ul[0] + cut_ratio*size, ul[1])
        fold_left = (ul[0], ul[1]-cut_ratio*size)
        fold_in = (fold_top[0], fold_left[1])
        fold_out_coords = [nump.c2p(*item) for item in [ul, fold_top, fold_left]]
        folded_out = Polygon(*fold_out_coords)
        fold_in_coords = [nump.c2p(*item) for item in [fold_top, fold_in, fold_left]]
        folded_in = Polygon(*fold_in_coords, stroke_width=3*size, color=GREY_C).set_fill(GREY_A, opacity=1)
        cut = Difference(paper, folded_out).set_fill(WHITE, opacity=1)
        self.add(cut)
        self.add(folded_in)

class Folder(VGroup):
    def __init__(self, size=3):
        super().__init__()
        h, w = size * 9 / 16 * 1.3, size
        folder = RoundedRectangle(size*0.05, height=h, width=w, color=YELLOW_B).set_fill(
            YELLOW_D, opacity=1
        )
        ratio = 0.4
        bh, bw = h*ratio, w*ratio
        back = RoundedRectangle(size*0.05, height=bh, width=bw, color=YELLOW_B).set_fill(
            YELLOW_E, opacity=1
        ).set_z_index(-0.01).align_to(folder, LEFT).align_to(folder, UP).shift(UP*size*0.15)
        self.add(folder, back)

class FileSystem(VGroup):
    def __init__(self, folders=[], files=[], tag: str | None = None, buff=0.25):
        super().__init__()
        folders_list = sorted(folders)
        files_list = sorted(files)

        self._folders = VGroup(*[FolderIcon(f) for f in folders_list]).arrange(DOWN, buff=buff, aligned_edge=LEFT)
        self._files = VGroup(*[FileIcon(f) for f in files_list]).arrange(DOWN, buff=buff, aligned_edge=LEFT)
        self.add(self._folders, self._files)
        self.arrange(DOWN, buff=buff, aligned_edge=LEFT)
        self._frame = RoundedRectangle(0.2, height=self.height, width=self.width, color=GREY_C).surround(self, buff=1.25)
        self.add(self._frame)
        if tag is not None:
            self._tag = Text(tag, font="Consolas", font_size=24).next_to(self._frame, UP, buff=0.05).align_to(self._frame, LEFT)
            self.add(self._tag)
        else:
            self._tag = None
    
    @property
    def folders(self):
        return self._folders
    
    @property
    def files(self):
        return self._files
    
    @property
    def frame(self):
        return self._frame
    
    @property
    def tag(self):
        return self._tag

class FolderIcon(VGroup):
    def __init__(self, text:str):
        super().__init__()
        self._icon = Folder(size=0.5)
        self._text = Text(text, font="Consolas", font_size=24)
        self.add(self._icon, self._text)
        self.arrange(RIGHT, buff=0.15)
    
    @property
    def icon(self):
        return self._icon
    
    @property
    def text(self):
        return self._text

class FileIcon(VGroup):
    def __init__(self, text:str):
        super().__init__()
        self._icon = File(size=0.4)
        self._text = Text(text, font="Consolas", font_size=24)
        self.add(self._icon, self._text)
        self.arrange(RIGHT, buff=0.25)
    
    @property
    def icon(self):
        return self._icon
    
    @property
    def text(self):
        return self._text