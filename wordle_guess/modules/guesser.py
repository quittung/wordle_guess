import json
import os.path

from . import wordle
from .strategies import strategy as strat


def load_wordlist(filename: str = "words.json") -> dict[str, int]:
    path = os.path.join(os.path.dirname(__file__), "..", "data", filename)
    with open(path, "r", encoding="utf-8") as fobj:
        words = json.load(fobj)
    return words

class Guesser(object):
    def __init__(self, strategy: strat.Strategy) -> None:
        self.hints = wordle.WordleHint()
        self.wordlist = load_wordlist()
        self.strategy = strategy
        self.candidates = self.strategy.sort_initial(self.wordlist)

    def process_hint(self, guess: str, pattern: str):
        self.hints.update_data(guess, pattern)
        self.wordlist = wordle.search(self.wordlist, self.hints)
        self.candidates = self.strategy.sort_candidates(self.wordlist)
