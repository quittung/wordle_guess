from . import wordle, loader
from .strategies import strategy as strat

def load_wordlist() -> dict[str, int]:
    return loader.load_json("words.json")

class Guesser(object):
    def __init__(self, strategy: strat.Strategy, wordlist: dict[str, int] = None) -> None:
        self.hints = wordle.WordleHint()
        self.wordlist = wordlist if wordlist else load_wordlist()
        self.strategy = strategy
        self.candidates = self.strategy.sort_initial(self.wordlist)

    def process_hint(self, guess: str, pattern: str):
        self.hints.update_data(guess, pattern)
        self.wordlist = wordle.search(self.wordlist, self.hints)
        self.candidates = self.strategy.sort_candidates(self.wordlist)
