from dataclasses import dataclass
from typing import List, Callable
from .base import ViewmodelBase
from models import CodenameModel


@dataclass
class MainViewmodel(ViewmodelBase):

    words: List[str]
    model: CodenameModel
    update: Callable

    def __init__(self, model: CodenameModel) -> None:
        super().__init__(model)
        self.model = model
        self.words = model.board.words
        self.show_answers = False

    def bind_update(self, update):
        self.update = update

    def on_select_word(self, word: str):
        self.model.board.get_word(word)['is_selected'] = True
        self.show_answers = not self.show_answers
        self.update()
