from . import wordle, loader
from .strategies import strategy as strat


class Guesser(object):
    def __init__(self, strategy: strat.Strategy) -> None:
        self.hints = wordle.WordleHint()
        self.wordlist = loader.load_json("words.json")
        self.strategy = strategy
        self.candidates = self.strategy.sort_initial(self.wordlist)

    def process_hint(self, guess: str, pattern: str):
        self.hints.update_data(guess, pattern)
        self.wordlist = wordle.search(self.wordlist, self.hints)
        self.candidates = self.strategy.sort_candidates(self.wordlist)
