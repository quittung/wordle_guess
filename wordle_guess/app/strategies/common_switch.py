from . import strategy
from . import common_words, common_letters

class CommonSwitchStrategy(strategy.Strategy):
    def __init__(self) -> None:
        self.sub_strategy_words = common_words.CommonWordsStrategy()
        self.sub_strategy_letters = common_letters.CommonLettersStrategy()

    def score_word(self, word: str) -> float:
        return sum([self.letter_frequency[char] for char in set(word)])

    def sort_candidates(self, candidates: dict[str, int]) -> list[str]:
        if len(candidates) > 119: # optimized value for 2000 most common five letter words
            return self.sub_strategy_letters.sort_candidates(candidates)
        else:
            return self.sub_strategy_words.sort_candidates(candidates)