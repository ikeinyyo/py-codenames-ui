from dataclasses import dataclass
from tkinter import *
from turtle import bgcolor, width

from viewmodels import MainViewmodel

from .base import (ViewBase, RoundedButton, center_window,
                   get_word_background_color, get_word_foreground_color,
                   BACKGROUND_COLOR, FORM_BG, FORM_BG_ACCENT_COLOR, FORM_LABEL_FG)


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
        self.window.resizable(False, False)
        self.board_frame = Frame(
            self.window, width=width, height=height, bg=BACKGROUND_COLOR)
        self.board_frame.grid(row=0, column=0)
        form = Frame(
            self.window, width=width, height=100, bg=FORM_BG)
        form.grid(row=1, column=0, sticky='ns')

        line = Frame(
            form, width=width, height=10, bg=FORM_BG_ACCENT_COLOR)

        form_controls = Frame(form, width=width/2, bg=FORM_BG)
        form_controls.grid(row=1, column=0, sticky='we')

        marker = Frame(form, bg='#222')
        marker.grid(row=1, column=1, sticky='we')

        if self.viewmodel.is_running:
            if self.viewmodel.show_clue:
                self.show_clue(form, line, form_controls, width)
            else:
                self.request_clue(form, line, form_controls, width)

        # Marcador
        self.red_label = Label(marker, text="9".upper(),
                               bg=FORM_BG, fg=FORM_LABEL_FG, font=('Arial', 18))
        self.red_label.grid(column=0, row=0, sticky='w')
        self.blue_label = Label(marker, text="8".upper(),
                                bg=FORM_BG, fg=FORM_LABEL_FG, font=('Arial', 18))
        self.blue_label.grid(column=1, row=0, sticky='w')
        self.neutral_label = Label(marker, text="7".upper(),
                                   bg=FORM_BG, fg=FORM_LABEL_FG, font=('Arial', 18))
        self.neutral_label.grid(column=2, row=0, sticky='w')
        self.murderer_label = Label(marker, text="1".upper(),
                                    bg=FORM_BG, fg=FORM_LABEL_FG, font=('Arial', 18))
        self.murderer_label.grid(column=3, row=0, sticky='w')

        center_window(self.window)

    def request_clue(self, form, line, form_controls, width):
        self.entry = Entry(form_controls)
        self.label = Label(form_controls, text="Insert a clue:".upper(),
                           bg=FORM_BG, fg=FORM_LABEL_FG, font=('Arial', 18))
        line.grid(row=0, column=0, columnspan=2)
        self.label.grid(row=1, column=0, padx=self.CELL_PADDING*2,
                        pady=self.CELL_PADDING, sticky='w')
        self.entry.grid(row=2, column=0, padx=self.CELL_PADDING*2,
                        pady=self.CELL_PADDING*2, sticky='w')

        Frame(
            form, width=width, height=50, bg=FORM_BG_ACCENT_COLOR).grid(row=3, column=0, columnspan=2)
        self.entry.bind('<Return>', self.on_entry_input)

    def show_clue(self, form, line, form_controls, width):
        self.clue_label = Label(form_controls, text=f"{self.viewmodel.model.current_clue.upper()} {self.viewmodel.model.clue_count}",
                                bg=FORM_BG, fg=FORM_LABEL_FG, font=('Arial', 18))
        self.label = Label(form_controls, text="Current clue:".upper(),
                           bg=FORM_BG, fg=FORM_LABEL_FG, font=('Arial', 18))
        line.grid(row=0, column=0, columnspan=2)
        self.label.grid(row=1, column=0, padx=self.CELL_PADDING*2,
                        pady=self.CELL_PADDING, sticky='w')
        self.clue_label.grid(row=2, column=0, padx=self.CELL_PADDING*2,
                             pady=self.CELL_PADDING*2, sticky='w')
        Frame(
            form, width=width, height=50, bg=FORM_BG_ACCENT_COLOR).grid(row=3, column=0, columnspan=2)

    def on_entry_input(self, _):
        clue = self.entry.get()
        self.viewmodel.set_clue(clue)
        self.entry.delete(0, 'end')

    def update(self):
        self.__initialize_window()
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
        self.red_label.config(text=len(list(filter(
            lambda word: word['team'] == 'red' and not word['is_selected'], self.viewmodel.words))))
        self.blue_label.config(text=len(list(filter(
            lambda word: word['team'] == 'blue' and not word['is_selected'], self.viewmodel.words))))
        self.neutral_label.config(text=len(list(filter(
            lambda word: word['team'] == 'neutral' and not word['is_selected'], self.viewmodel.words))))
        self.murderer_label.config(text=len(list(filter(
            lambda word: word['team'] == 'murderer' and not word['is_selected'], self.viewmodel.words))))

    def run(self):
        self.window.mainloop()
