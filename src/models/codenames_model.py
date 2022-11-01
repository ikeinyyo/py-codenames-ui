import random
from dataclasses import dataclass

from .base import ModelBase
from .components import Board


@dataclass
class CodenameModel(ModelBase):
    board: Board
    rows: int
    columns: int

    def __init__(self, language_code, rows, columns) -> None:
        self.rows = rows
        self.columns = columns
        red_goes_first = random.choice([True, False])
        self.board = Board(language_code, red_goes_first, rows, columns)
