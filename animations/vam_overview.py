"""A plain-language, captioned introduction to tomographic VAM, made in Manim.

Render from the repository root:
    manim -qh --fps 30 animations/vam_overview.py VAMOverview

The light patterns and two sample regions are explanatory illustrations, not
optimized projection data or a calibrated polymerization simulation.
"""

from manim import *
import numpy as np


PAPER = "#FAFAF7"
INK = "#202C34"
MUTED = "#657780"
LINE = "#A9BDC5"
RESIN = "#BFDDE5"
PART = "#2D7491"
LIGHT = "#886CC4"
FONT = "DejaVu Sans"


def words(text, size=24, color=INK, bold=False):
    return Text(text, font=FONT, font_size=size, color=color,
                weight="BOLD" if bold else "NORMAL", disable_ligatures=True)


def projected_ring(angle=0, scale=1, center=ORIGIN, opacity=1):
    """A shaded upright torus, projected into the scene's fixed 2D view."""
    us = np.linspace(0, TAU, 41)
    vs = np.linspace(0, TAU, 13)
    ca, sa = np.cos(angle), np.sin(angle)
    rotation = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
    sun = np.array([-0.5, -0.9, 1.3])
    sun /= np.linalg.norm(sun)
    faces = []

    def point(u, v):
        return rotation @ np.array([(0.88 + 0.25*np.cos(v))*np.cos(u),
                                    0.25*np.sin(v),
                                    (0.88 + 0.25*np.cos(v))*np.sin(u)])

    def project(p):
        return np.array([0.94*p[0]+0.34*p[1],
                         0.95*p[2]-0.24*p[1]+0.06*p[0], 0])*scale+center

    for u0, u1 in zip(us[:-1], us[1:]):
        for v0, v1 in zip(vs[:-1], vs[1:]):
            pts = [point(u0, v0), point(u1, v0), point(u1, v1), point(u0, v1)]
            u, v = (u0+u1)/2, (v0+v1)/2
            normal = rotation @ np.array([np.cos(v)*np.cos(u), np.sin(v),
                                           np.cos(v)*np.sin(u)])
            brightness = 0.28+0.72*max(0, np.dot(normal, sun))
            shade = interpolate_color(ManimColor("#123C51"),
                                      ManimColor("#9AC7D5"), brightness)
            face = Polygon(*[project(p) for p in pts], stroke_width=0.35,
                           stroke_color=shade, fill_color=shade,
                           fill_opacity=opacity, stroke_opacity=opacity)
            depth = np.dot(np.mean(pts, axis=0), np.array([0.34, -0.94, 0.24]))
            faces.append((depth, face))
    return VGroup(*[f for _, f in sorted(faces, key=lambda x: x[0])])


def vessel(center=ORIGIN, scale=1):
    """Back and front of a transparent vessel, so parts sit inside it."""
    x, y = center[:2]
    w, h, e = 2.9*scale, 3.8*scale, 0.48*scale
    body = Rectangle(width=w, height=h, stroke_width=0,
                     fill_color=RESIN, fill_opacity=0.19).move_to(center)
    liquid_top = Ellipse(width=w, height=e, stroke_color=LINE, stroke_width=1,
                         fill_color=RESIN, fill_opacity=0.35).move_to([x, y+1.25*scale, 0])
    liquid = Rectangle(width=w, height=3.15*scale, stroke_width=0,
                       fill_color=RESIN, fill_opacity=0.15).move_to([x, y-0.325*scale, 0])
    back = VGroup(body, liquid, liquid_top)
    top = Ellipse(width=w, height=e, color=LINE, stroke_width=1.8).move_to([x,y+h/2,0])
    base = Ellipse(width=w, height=e, color=LINE, stroke_width=1.8).move_to([x,y-h/2,0])
    sides = VGroup(Line([x-w/2,y-h/2,0],[x-w/2,y+h/2,0],color=LINE,stroke_width=1.8),
                   Line([x+w/2,y-h/2,0],[x+w/2,y+h/2,0],color=LINE,stroke_width=1.8))
    front = VGroup(base, sides, top)
    return back, front


def pattern(angle, size=90):
    """An illustrative projection of an upright ring onto a detector plane."""
    axis = np.linspace(-1.4, 1.4, size)
    xx, yy, zz = np.meshgrid(axis, axis, axis, indexing="ij")
    ca, sa = np.cos(angle), np.sin(angle)
    xr, yr = ca*xx+sa*yy, -sa*xx+ca*yy
    volume = (np.sqrt(xr*xr+zz*zz)-0.88)**2+yr*yr < 0.25**2
    image = volume.sum(axis=1).T[::-1].astype(float)
    image /= max(1, image.max())
    image = np.power(image, 0.65)
    rgb = np.zeros((size, size, 4), dtype=np.uint8)
    rgb[:, :, :3] = (np.array([171, 144, 231])[None,None,:]*image[:,:,None]).astype(np.uint8)
    rgb[:, :, 3] = 255
    return rgb


def pattern_card(angle, center, width=1.7):
    frame = Square(side_length=width, stroke_color=LINE, stroke_width=1,
                   fill_color="#18232C",fill_opacity=1).move_to(center)
    image = ImageMobject(pattern(angle)).set_width(width-0.12).move_to(center)
    return Group(frame, image)


class VAMOverview(Scene):
    def setup(self):
        self.camera.background_color = PAPER
        self.credit = words("Jocabe", 15, MUTED).to_corner(DR, buff=0.34)
        self.credit.set_z_index(100)
        self.add(self.credit)

    def clear_stage(self):
        old = [m for m in self.mobjects if m is not self.credit]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=0.65)

    def heading(self, text):
        title = words(text, 32, bold=True).to_edge(UP,buff=0.52).to_edge(LEFT,buff=0.72)
        self.play(FadeIn(title,shift=0.08*UP),run_time=0.6)
        return title

    def caption(self, lines):
        caption = VGroup(*[words(line,23) for line in lines]).arrange(DOWN,buff=0.16)
        caption.move_to([0,-2.9,0])
        self.play(FadeIn(caption),run_time=0.5)
        return caption

    def construct(self):
        # 1. A useful first frame, including a real view of the example part.
        title = VGroup(words("Printing",50,bold=True),
                       words("with light.",50,bold=True)).arrange(DOWN,aligned_edge=LEFT,buff=0.14)
        title.move_to([-3.2,0.65,0])
        subtitle = VGroup(words("Volumetric additive",23,MUTED),
                          words("manufacturing · VAM",23,MUTED)).arrange(DOWN,aligned_edge=LEFT,buff=0.12)
        subtitle.next_to(title,DOWN,aligned_edge=LEFT,buff=0.5)
        method = words("A rotating-vat method",18,MUTED).next_to(subtitle,DOWN,aligned_edge=LEFT,buff=0.25)
        ring = projected_ring(-0.35,1.7,np.array([3.05,0.35,0]))
        self.add(title,subtitle,method,ring)
        self.wait(3.7)
        intro = words("A 3D shape formed inside a liquid.",24).move_to([0,-2.7,0])
        self.play(FadeIn(intro),run_time=0.6)
        self.wait(2.2)
        self.clear_stage()

        # 2. Introduce the layer-free distinction without promises about speed.
        self.heading("A different way to make a 3D object.")
        left_label = words("Layer by layer",22,MUTED).move_to([-3.3,1.9,0])
        right_label = words("Inside a volume",22,MUTED).move_to([3.15,1.9,0])
        self.play(FadeIn(left_label),FadeIn(right_label),run_time=0.5)
        stack = VGroup(*[RoundedRectangle(width=2.35,height=0.15,corner_radius=0.035,
                                         color=PART,stroke_width=1,
                                         fill_color=PART,fill_opacity=0.65)
                          .move_to([-3.3,-1.1+i*0.16,0]) for i in range(13)])
        back, front = vessel(np.array([3.15,-0.35,0]),0.77)
        self.play(FadeIn(back),Create(front),run_time=0.8)
        self.play(LaggedStart(*[FadeIn(layer) for layer in stack],lag_ratio=0.15),run_time=2.5)
        part = projected_ring(-0.2,0.78,np.array([3.15,-0.4,0]))
        self.play(FadeIn(part),run_time=2)
        self.caption(["Many printers build one layer at a time.",
                      "VAM forms the part throughout a volume of resin."])
        self.wait(3.3)
        self.clear_stage()

        # 3. Show that calculated 2D patterns come from a 3D design.
        self.heading("First, start with a digital model.")
        model = projected_ring(-0.3,1.05,np.array([-4.4,0,0]))
        cards = Group(*[pattern_card(a,np.array([x,0,0]))
                        for a,x in zip([0,0.7,1.3],[0,2.1,4.2])])
        arrow = Arrow([-2.6,0,0],[-1.25,0,0],buff=0,color=LINE,stroke_width=2)
        self.play(FadeIn(model),run_time=0.9)
        self.play(GrowArrow(arrow),LaggedStart(*[FadeIn(c) for c in cards],lag_ratio=0.3),run_time=1.6)
        labels = VGroup(words("3D model",20,MUTED).move_to([-4.4,-1.55,0]),
                        words("Calculated light patterns",20,MUTED).move_to([2.1,-1.55,0]))
        self.play(FadeIn(labels),run_time=0.5)
        self.caption(["Software calculates a different light pattern", "for each viewing angle."])
        self.wait(4.3)
        self.clear_stage()

        # 4. One stationary projector; resin and vial rotate together.
        self.heading("The container turns. The pattern changes.")
        back,front = vessel(np.array([2.25,0.05,0]),0.9)
        projector = VGroup(RoundedRectangle(width=1.45,height=0.85,corner_radius=0.08,
                                           color=LINE,stroke_width=2,fill_color=WHITE,fill_opacity=1),
                           Circle(radius=0.19,stroke_color=LIGHT,stroke_width=2,
                                  fill_color=LIGHT,fill_opacity=0.2).shift(0.65*RIGHT))
        projector.move_to([-4.6,-0.05,0])
        beam = Polygon([-3.75,0.18,0],[0.94,1.34,0],[0.94,-1.34,0],[-3.75,-0.18,0],
                       stroke_width=0,fill_color=LIGHT,fill_opacity=0.09)
        beam_inside = Rectangle(width=2.58,height=2.66,stroke_width=0,
                                fill_color=LIGHT,fill_opacity=0.055).move_to([2.25,0,0])
        self.play(FadeIn(back),Create(front),FadeIn(projector),run_time=0.8)
        self.play(FadeIn(beam),FadeIn(beam_inside),run_time=0.6)
        label1=words("Projector",19,MUTED).next_to(projector,DOWN,buff=0.3)
        label2=words("Light-sensitive liquid resin",19,MUTED).move_to([2.25,-2.05,0])
        self.play(FadeIn(label1),FadeIn(label2),run_time=0.4)
        marker = Dot([3.35,1.25,0],radius=0.06,color=PART)
        turn = CurvedArrow([3.8,-1.1,0],[3.8,1.15,0],angle=PI/2,color=MUTED,stroke_width=1.5,tip_length=0.12)
        self.add(marker)
        self.play(Create(turn),run_time=0.5)
        screen = pattern_card(0,np.array([-1.6,0,0]),1.45)
        self.play(FadeIn(screen),run_time=0.5)
        self.caption(["The changing patterns shine through the liquid.",
                      "Rotation lets the light reach it from many angles."])
        for index in range(1,9):
            angle=index*TAU/8
            target=pattern_card(angle,np.array([-1.6,0,0]),1.45)
            self.play(FadeOut(screen), FadeIn(target),
                      MoveAlongPath(marker,ParametricFunction(
                          lambda t, a=(index-1)*TAU/8: np.array([2.25+1.1*np.cos(a+t*TAU/8),
                                                                1.25+0.18*np.sin(a+t*TAU/8),0]),
                          t_range=[0,1])),
                      run_time=0.95,rate_func=linear)
            screen=target
        self.wait(1.5)
        self.clear_stage()

        # 5. A conceptual close-up of two regions, with no numerical readouts.
        self.heading("The light adds up.")
        region1=Circle(radius=0.95,color=LINE,stroke_width=1.5,
                       fill_color=RESIN,fill_opacity=0.5).move_to([-2.6,0.2,0])
        region2=region1.copy().move_to([2.6,0.2,0])
        labels=VGroup(words("Inside the intended part",20,MUTED).move_to([-2.6,1.7,0]),
                      words("Outside the part",20,MUTED).move_to([2.6,1.7,0]))
        self.play(FadeIn(region1),FadeIn(region2),FadeIn(labels),run_time=0.8)
        self.caption(["Enough accumulated light turns the resin solid.",
                      "The surrounding resin stays below that threshold."])
        for i in range(6):
            pulse1=Circle(radius=0.28,color=LIGHT,stroke_width=0,
                          fill_color=LIGHT,fill_opacity=0.65).move_to([-4.4,0.2,0])
            animations=[FadeIn(pulse1)]
            pulse2=None
            if i in [1,4]:
                pulse2=pulse1.copy().move_to([4.4,0.2,0])
                animations.append(FadeIn(pulse2))
            self.play(*animations,run_time=0.15)
            animations=[pulse1.animate.move_to(region1.get_center()).set_opacity(0),
                        region1.animate.set_fill(interpolate_color(ManimColor(RESIN),ManimColor(PART),(i+1)/6),opacity=0.9)]
            if pulse2 is not None:
                animations.append(pulse2.animate.move_to(region2.get_center()).set_opacity(0))
            self.play(*animations,run_time=0.7)
            self.remove(pulse1)
            if pulse2 is not None: self.remove(pulse2)
        state1=words("Solid",23,PART,bold=True).move_to([-2.6,-1.3,0])
        state2=words("Still liquid",23,MUTED).move_to([2.6,-1.3,0])
        self.play(FadeIn(state1),FadeIn(state2),region1.animate.set_stroke(PART,width=2),run_time=0.7)
        self.wait(3.3)
        self.clear_stage()

        # 6. The solid part appears in the volume, then is separated from resin.
        self.heading("A solid shape appears inside the liquid.")
        back,front=vessel(np.array([-2.8,0,0]),0.88)
        part=projected_ring(-0.2,0.9,np.array([-2.8,0,0]))
        self.play(FadeIn(back),Create(front),run_time=0.7)
        self.play(FadeIn(part),run_time=2.4)
        self.caption(["Remove the part, then drain and rinse away", "the uncured resin."])
        arrow=Arrow([-0.9,0.15,0],[1.2,0.15,0],color=LINE,stroke_width=2,buff=0.15)
        self.play(GrowArrow(arrow),run_time=0.6)
        self.play(part.animate.shift(5.6*RIGHT).scale(1.35),run_time=2.5)
        self.wait(2.7)
        self.clear_stage()

        # 7. A quiet final recap, with the same small corner credit.
        headline=words("A whole 3D shape.",38,bold=True).move_to([0,2.55,0])
        sub=words("No layer-by-layer stacking.",25,MUTED).move_to([0,1.75,0])
        final_part=projected_ring(-0.35,1.2,np.array([0,-0.2,0]))
        recap=words("3D model  →  light patterns  →  solid part",23).move_to([0,-2.35,0])
        self.play(FadeIn(headline),FadeIn(sub),FadeIn(final_part),run_time=1)
        self.play(FadeIn(recap),run_time=0.6)
        self.wait(4.5)

