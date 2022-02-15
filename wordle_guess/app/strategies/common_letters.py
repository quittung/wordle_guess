from . import strategy
from .. import loader

class CommonLettersStrategy(strategy.Strategy):
    def __init__(self) -> None:
        self.letter_frequency = loader.load_json("letter_freq.json")

    def score_word(self, word: str) -> float:
        return sum([self.letter_frequency[char] for char in set(word)])

    def sort_candidates(self, candidates: dict[str, int]) -> list[str]:
        candidates_scored = {word: self.score_word(word) for word in candidates}
        return list(sorted(candidates_scored.keys(), key=lambda k: candidates_scored[k], reverse=True))