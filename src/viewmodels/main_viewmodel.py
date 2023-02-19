from dataclasses import dataclass
from typing import List, Callable
from .base import ViewmodelBase
from models import CodenameModel
from enum import Enum


@dataclass
class MainViewmodel(ViewmodelBase):
    class States(Enum):
        ANSWER = "ANSWER"
        CLUE = "CLUE"
        CREATE_LOG = "CREATE_LOG"
        CHANGE_TEAM = "CHANGE_TEAM"
        WIN = "WIN"
        LOSE = "LOSE"
        FINISH = "FINISH"

    words: List[str]
    model: CodenameModel
    update: Callable
    show_clue: bool
    is_running: bool
    is_red_turn: bool

    def __init__(self, model: CodenameModel) -> None:
        super().__init__(model)
        self.model = model
        self.is_red_turn = self.model.red_goes_first
        self.words = model.board.words
        self.is_running = True
        self.set_request_clue()

    def bind_update(self, update):
        self.update = update

    def set_clue(self, clue):
        print(clue)
        self.model.current_clue = clue.split()[0]
        self.model.clue_count = int(clue.split()[1])
        self.show_clue = True
        self.show_answers = False
        self.update()

    def on_select_word(self, word: str):
        self.check_answer(word)
        self.model.board.get_word(word)['is_selected'] = True
        self.update()

    def set_request_clue(self):
        # if boss is a bot. Make request and call set_clue
        self.show_answers = True
        self.show_clue = False

    def set_show_clue(self):
        # if boss is a bot. Make request and call on_select_word
        self.show_answers = False
        self.show_clue = True

    def change_team(self):
        self.is_red_turn = not self.is_red_turn
        self.set_request_clue()

    def correct_answer(self):
        if self.model.clue_count <= 0:
            self.change_team()
        else:
            self.model.clue_count -= 1

    def end_game(self):
        self.is_running = False

    def check_answer(self, answer):
        word = self.model.board.get_word(answer)
        if word['team'] == 'red' and self.is_red_turn or word['team'] == 'blue' and not self.is_red_turn:
            self.correct_answer()
        elif word['team'] == 'murderer':
            self.end_game()
        else:
            self.change_team()
