from dataclasses import dataclass
from viewmodels.base import ViewmodelBase


@dataclass
class ViewBase:
    viewmodel: ViewmodelBase

    def __init__(self, viewmodel: ViewmodelBase) -> None:
        self.viewmodel = viewmodel
