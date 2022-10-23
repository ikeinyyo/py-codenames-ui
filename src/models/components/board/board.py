import json
import os
import random
from dataclasses import dataclass
from typing import List


@dataclass
class Board:
    words: List[dict]

    def __init__(self, language_code, red_goes_first) -> None:
        self.__create_board(language_code, red_goes_first)

    def get_word(self, word):
        return list(filter(lambda board_word: board_word['word'].lower() == word.lower(), self.words))[0]

    @staticmethod
    def __load_words(language: str) -> List[str]:
        file_name = f"{os.path.dirname(__file__)}/data/{language}.words.json"
        with open(file_name, 'r', encoding='utf-8') as in_file:
            words = json.load(in_file)['words']
            random.shuffle(words)
            return words[:25]

    def __create_board(self, language_code: str, red_goes_first: bool) -> None:
        words = self.__load_words(language_code)
        red = words[:9 if red_goes_first else 8]
        blue = words[9 if red_goes_first else 8:17]
        neutral = words[17:24]
        murderer = [words[-1]]
        self.words = [*Board.__initialize_words(red, 'red'), *Board.__initialize_words(
            blue, 'blue'), *Board.__initialize_words(neutral, 'neutral'), *Board.__initialize_words(murderer, 'murderer'), ]
        random.shuffle(self.words)

    @staticmethod
    def __initialize_words(words, team):
        return list(map(lambda word: {'word': word, 'team': team, 'is_selected': False}, words))
