from manim import *

get_commit = lambda: Circle(radius=0.15, color=WHITE, fill_color=BLACK, fill_opacity=1)
chash = lambda text: Text(text, font_size=24, color=RED)

def new_commit(from_commit, *, direction=RIGHT, buff=1):
    newc = get_commit().next_to(from_commit, direction=direction, buff=buff)
    start = from_commit.get_corner(direction)
    to = newc.get_corner(-direction)
    cline = Line(start, to, color=GREY_C)
    return newc, cline

def branch(start=None, *, direction=RIGHT, n_commits=3, buff=1):
    s = start or get_commit()
    commits = VGroup(VGroup(s, VMobject()))
    for i in range(n_commits):
        if i == 0 and start is not None:
            offset = direction + np.array([-direction[1], direction[0], 0])
            c, l = new_commit(s, direction=offset, buff=buff)
        else:
            c, l = new_commit(commits[-1][0], direction=direction, buff=buff)
        commits.add(VGroup(c, l))
    return commits