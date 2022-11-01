import json
import os
import random
from dataclasses import dataclass
from typing import List


@dataclass
class Board:
    words: List[dict]

    def __init__(self, language_code, red_goes_first, rows, columns) -> None:
        self.__create_board(language_code, red_goes_first, rows, columns)

    def get_word(self, word):
        return list(filter(lambda board_word: board_word['word'].lower() == word.lower(), self.words))[0]

    @staticmethod
    def __load_words(language: str, rows: int, columns: int) -> List[str]:
        file_name = f"{os.path.dirname(__file__)}/data/{language}.words.json"
        with open(file_name, 'r', encoding='utf-8') as in_file:
            words = json.load(in_file)['words']
            random.shuffle(words)
            return words[:rows*columns]

    def __create_board(self, language_code: str, red_goes_first: bool, rows: int, columns: int) -> None:
        words = self.__load_words(language_code, rows, columns)
        # calculate the ratio using 5x5 game
        num_words = int(8/25 * rows*columns)
        red = words[:num_words+1 if red_goes_first else num_words]
        blue = words[num_words +
                     1 if red_goes_first else num_words:num_words+num_words+1]
        neutral = words[num_words+num_words+1:-1]
        murderer = [words[-1]]
        self.words = [*Board.__initialize_words(red, 'red'), *Board.__initialize_words(
            blue, 'blue'), *Board.__initialize_words(neutral, 'neutral'), *Board.__initialize_words(murderer, 'murderer'), ]
        random.shuffle(self.words)

    @staticmethod
    def __initialize_words(words, team):
        return list(map(lambda word: {'word': word, 'team': team, 'is_selected': False}, words))
