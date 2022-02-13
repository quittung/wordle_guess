import os.path
import json

from . import strategy

class UnusualThenCommonStrategy(strategy.Strategy):
    def __init__(self) -> None:
        path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "letter_freq.json")
        with open(path, "r", encoding="utf-8") as fobj:
            self.letter_frequency = json.load(fobj)

    def score_word(self, word: str) -> float:
        return sum([self.letter_frequency[char] for char in set(word)])

    def sort_candidates(self, candidates: dict[str, int]) -> list[str]:
        if len(candidates) > 119: # optimized value for 2000 most common five letter words
            candidates_scored = {word: self.score_word(word) for word in candidates}
            return list(sorted(candidates_scored.keys(), key=lambda k: candidates_scored[k], reverse=True))
        else:
            return list(sorted(candidates.keys(), key=lambda k: candidates[k], reverse=True))