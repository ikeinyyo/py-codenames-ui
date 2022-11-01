from tkinter import *


class RoundedButton(Canvas):
    def __init__(self, parent, height,
                 width, border_radius, bg, fg, font=("Arial", 25), text='', command=None):
        Canvas.__init__(self, parent, borderwidth=0,
                        relief="raised", highlightthickness=0, bg=parent["bg"])
        self.command = command
        self.id = None
        self.text = text

        width = width if width >= 80 else 80

        if border_radius > 0.5*width:
            print("Error: border_radius is greater than width.")
            return None

        if border_radius > 0.5*height:
            print("Error: border_radius is greater than height.")
            return None

        rad = 2*border_radius

        def shape():
            self.create_arc((0, rad, rad, 0),
                            start=90, extent=90, fill=bg, outline=bg)
            self.create_arc((width-rad, 0, width,
                             rad), start=0, extent=90, fill=bg, outline=bg)
            self.create_arc((width, height-rad, width-rad,
                             height), start=270, extent=90, fill=bg, outline=bg)
            self.create_arc((0, height-rad, rad, height),
                            start=180, extent=90, fill=bg, outline=bg)
            return self.create_polygon((0, height-border_radius, 0, border_radius, border_radius, 0, width-border_radius, 0, width,
                                        border_radius, width, height-border_radius, width-border_radius, height, border_radius, height),
                                       fill=bg, outline=bg)

        self.id = shape()
        (x0, y0, x1, y1) = self.bbox("all")
        width = (x1-x0)
        height = (y1-y0)
        self.configure(width=width, height=height)
        self.create_text(width/2, height/2, text=text,
                         fill=fg, font=font)
        self.bind("<1>", self._on_press)

    def _on_press(self, _):
        self.command(self.text)
