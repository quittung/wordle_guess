"""handles scoring how common the characters in a word are"""

def load_freqs(filename):
    with open(filename, 'r', encoding="utf-8") as fobj:
        lines = [line.split(",") for line in fobj]

    return {line[0]: float(line[1]) for line in lines}


def score_word(word: str, freqs: dict[str, float]) -> float:
    return sum([freqs[char] for char in set(word)])


class Scorer(object):
    def __init__(self, filename: str = "common/letter_freq.csv"):
        self.freqs = load_freqs(filename)
    def __call__(self, word):
        return score_word(word, self.freqs)