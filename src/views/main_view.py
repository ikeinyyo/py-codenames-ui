from dataclasses import dataclass
from tkinter import *
from turtle import width

from viewmodels import MainViewmodel

from .base import (ViewBase, RoundedButton, center_window,
                   get_word_background_color, get_word_foreground_color,
                   BACKGROUND_COLOR)


@dataclass
class MainView(ViewBase):
    window: Tk
    board_frame: Frame
    CELL_HEIGHT: int = 100
    CELL_WIDTH: int = 200
    CELL_PADDING: int = 4

    def __init__(self, viewmodel: MainViewmodel) -> None:
        super().__init__(viewmodel)
        self.rows = self.viewmodel.model.rows
        self.columns = self.viewmodel.model.columns
        self.window = Tk()
        self.__initialize_window()
        self.update()
        self.viewmodel.bind_update(self.update)

    def __initialize_window(self):
        self.window.configure(bg=BACKGROUND_COLOR)
        self.window.title("Py-Codename")
        width = (self.CELL_WIDTH + self.CELL_PADDING*3)*self.columns
        height = (self.CELL_HEIGHT + self.CELL_PADDING*3)*self.rows
        self.window.geometry(
            f"{width}x{height + 100}")
        #self.window.resizable(False, False)
        self.board_frame = Frame(
            self.window, width=width, height=height, bg=BACKGROUND_COLOR)
        self.board_frame.grid(row=0, column=0)
        center_window(self.window)

    def update(self):
        self.__clear_board()
        self.__show_board()

    def on_word_click(self, text):
        self.viewmodel.on_select_word(text)

    def __clear_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

    def __show_board(self):
        for row in range(self.rows):
            for column in range(self.columns):
                word = self.viewmodel.words[row*self.columns+column]
                button = RoundedButton(self.board_frame, width=self.CELL_WIDTH, height=self.CELL_HEIGHT,
                                       text=word['word'].upper(), border_radius=10,
                                       command=self.on_word_click,
                                       bg=get_word_background_color(self.viewmodel.show_answers,
                                                                    word),
                                       fg=get_word_foreground_color(self.viewmodel.show_answers, word))
                button.grid(row=row, column=column, padx=self.CELL_PADDING,
                            pady=self.CELL_PADDING)

    def run(self):
        self.window.mainloop()
