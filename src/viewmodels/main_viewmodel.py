from dataclasses import dataclass
from typing import List, Callable
from .base import ViewmodelBase
from models import CodenameModel


@dataclass
class MainViewmodel(ViewmodelBase):

    words: List[str]
    update: Callable

    def __init__(self, model: CodenameModel) -> None:
        super().__init__(model)
        self.words = model.board.words

    def bind_update(self, update):
        self.update = update

    def on_select_word(self, word: str):
        print(word)
        self.update()
