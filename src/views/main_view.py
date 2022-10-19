from dataclasses import dataclass
from tkinter import *

from viewmodels import MainViewmodel

from .base import ViewBase


@dataclass
class MainView(ViewBase):
    window: Tk
    board_frame: Frame
    CELL_HEIGHT: int = 100
    CELL_WIDTH: int = 200

    def __init__(self, viewmodel: MainViewmodel) -> None:
        super().__init__(viewmodel)
        self.window = Tk()
        self.__initialize_window()
        self.update()
        self.viewmodel.bind_update(self.update)

    def __initialize_window(self):
        self.window.title("Py-Codename")
        self.window.geometry(f"{self.CELL_WIDTH*5}x{self.CELL_HEIGHT*5 + 100}")
        self.window.resizable(False, False)
        self.board_frame = Frame(
            self.window, height=self.CELL_HEIGHT*5, width=self.CELL_WIDTH*5)
        self.board_frame.grid(row=0, column=0)
        MainView.center(self.window)

    def update(self):
        self.clear_board()
        self.show_board()

    def on_word_click(self, event):
        self.viewmodel.on_select_word(event.widget.cget("text"))

    def clear_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

    def show_board(self):

        for i in range(5):
            for j in range(5):
                frame = Frame(self.board_frame, height=self.CELL_HEIGHT, width=self.CELL_WIDTH,
                              bg='blue' if (j+i) % 2 == 0 else 'yellow')
                frame.pack_propagate(False)
                frame.grid(row=i, column=j)
                label = Label(frame, text=self.viewmodel.words[i*5+j].upper(), background='blue' if (
                    j+i) % 2 == 0 else 'yellow', font=("Arial", 25))
                label.pack(fill=BOTH, expand=1)
                label.bind("<1>", self.on_word_click)

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
