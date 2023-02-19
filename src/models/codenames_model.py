import random
from dataclasses import dataclass

from .base import ModelBase
from .components import Board


@dataclass
class CodenameModel(ModelBase):

    board: Board
    rows: int
    columns: int
    current_clue: str
    clue_count: str
    red_goes_first: bool

    def __init__(self, language_code, rows=5, columns=5) -> None:
        self.rows = rows
        self.columns = columns
        self.current_clue = ""
        self.clue_count = 0
        self.red_goes_first = random.choice([True, False])
        self.board = Board(language_code, self.red_goes_first, rows, columns)
