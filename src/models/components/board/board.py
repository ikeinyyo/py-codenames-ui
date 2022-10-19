import json
import os
import random
from dataclasses import dataclass
from typing import List


@dataclass
class Board:
    words: List[str]
    red: List[str]
    blue: List[str]
    neutral: List[str]
    murderer: List[str]
    selected_words: List[str]

    def __init__(self, language_code, red_goes_first) -> None:
        self.__create_board(language_code, red_goes_first)

    @staticmethod
    def __load_words(language: str) -> List[str]:
        file_name = f"{os.path.dirname(__file__)}/data/{language}.words.json"
        with open(file_name, 'r', encoding='utf-8') as in_file:
            words = json.load(in_file)['words']
            random.shuffle(words)
            return words[:25]

    def __create_board(self, language_code: str, red_goes_first: bool) -> None:
        self.words = self.__load_words(language_code)
        self.red = self.words[:9 if red_goes_first else 8]
        self.blue = self.words[9 if red_goes_first else 8:17]
        self.neutral = self.words[17:24]
        self.murderer = [self.words[-1]]
        self.selected_words = []
        random.shuffle(self.words)
