from dataclasses import dataclass
from tkinter import *
from turtle import width

from viewmodels import MainViewmodel

from .base import ViewBase
import tkinter.font as font


class RoundedButton(Canvas):
    def __init__(self, parent, border_radius, height, width, bg, fg, padding, text='', command=None):
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

        id = shape()
        (x0, y0, x1, y1) = self.bbox("all")
        width = (x1-x0)
        height = (y1-y0)
        self.configure(width=width, height=height)
        self.create_text(width/2, height/2, text=text,
                         fill=fg, font=("Arial", 25))
        self.bind("<1>", self._on_press)

    def _on_press(self, _):
        self.command(self.text)


@dataclass
class MainView(ViewBase):
    window: Tk
    board_frame: Frame
    CELL_HEIGHT: int = 100
    CELL_WIDTH: int = 200
    CELL_PADDING: int = 2

    def __init__(self, viewmodel: MainViewmodel) -> None:
        super().__init__(viewmodel)
        self.window = Tk()
        self.__initialize_window()
        self.update()
        self.viewmodel.bind_update(self.update)

    def __initialize_window(self):
        self.window.configure(bg="black")
        self.window.title("Py-Codename")
        self.window.geometry(
            f"{(self.CELL_WIDTH + self.CELL_PADDING*2)*5}x{(self.CELL_HEIGHT + self.CELL_PADDING*2)*5 + 100}")
        self.window.resizable(False, False)
        self.board_frame = Frame(
            self.window, height=self.CELL_HEIGHT*5, width=self.CELL_WIDTH*5, bg='black')
        self.board_frame.grid(row=0, column=0)
        MainView.center(self.window)

    def update(self):
        self.clear_board()
        self.show_board()

    def on_word_click(self, text):
        self.viewmodel.on_select_word(text)

    def clear_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

    def show_board(self):

        for i in range(5):
            for j in range(5):
                word = self.viewmodel.words[i*5+j]
                button = RoundedButton(self.board_frame, width=self.CELL_WIDTH, height=self.CELL_HEIGHT,
                                       text=word['word'].upper(), border_radius=10,
                                       padding=self.CELL_PADDING,
                                       command=self.on_word_click,
                                       bg=MainView.get_word_background_color(
                                           word),
                                       fg=MainView.get_word_foreground_color(word))
                button.grid(row=i, column=j, padx=self.CELL_PADDING,
                            pady=self.CELL_PADDING)
                '''
                frame = Frame(self.board_frame, height=self.CELL_HEIGHT, width=self.CELL_WIDTH,
                              bg=MainView.get_word_background_color(word))
                frame.pack_propagate(False)
                frame.grid(row=i, column=j, padx=self.CELL_PADDING,
                           pady=self.CELL_PADDING)
                label = Label(frame, text=word['word'].upper(
                ), background=MainView.get_word_background_color(word), font=("Arial", 25), fg=MainView.get_word_foreground_color(word))
                
                label.pack(fill=BOTH, expand=1)
                label.bind("<1>", self.on_word_click)
                '''

    @staticmethod
    def get_word_background_color(word):
        if not word['is_selected']:
            return {
                'red': '#4d1111',
                'blue': '#02344d',
                'murderer': '#262626'
            }.get(word['team'], '#4d4d4d')
        return {
            'red': '#f53333',
            'blue': '#0594e3',
            'murderer': '#111111'
        }.get(word['team'], '#eaece1')

    @staticmethod
    def get_word_foreground_color(word):
        if not word['is_selected']:
            return {
                'murderer': '#999999'
            }.get(word['team'], 'black')
        return {
            'murderer': 'white'
        }.get(word['team'], 'black')

    @staticmethod
    def center(win):
        """
        centers a tkinter window
        :param win: the main window or Toplevel window to center
        """
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

    def run(self):
        self.window.mainloop()
