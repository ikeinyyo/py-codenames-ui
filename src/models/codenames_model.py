import random
from dataclasses import dataclass

from .base import ModelBase
from .components import Board


@dataclass
class CodenameModel(ModelBase):
    board: Board

    def __init__(self, language_code) -> None:
        red_goes_first = random.choice([True, False])
        self.board = Board(language_code, red_goes_first)
