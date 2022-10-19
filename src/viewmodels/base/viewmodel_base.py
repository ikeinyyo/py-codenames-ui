from dataclasses import dataclass

from models.base import ModelBase


@dataclass
class ViewmodelBase:
    model: ModelBase

    def __init__(self, model: ModelBase) -> None:
        self.model = model
