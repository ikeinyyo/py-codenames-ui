from dataclasses import dataclass
from typing import List
from .base import ViewmodelBase
from models import CodenameModel


@dataclass
class MainViewmodel(ViewmodelBase):

    words: List[str]

    def __init__(self, model: CodenameModel) -> None:
        super().__init__(model)
        self.words = model.board.words
