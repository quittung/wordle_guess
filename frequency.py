def load_freqs(filename: str = "letter_freq.csv"):
    with open(filename, 'r', encoding="utf-8") as fobj:
        lines = [line.split(",") for line in fobj]

    return {line[0]: float(line[1]) for line in lines}

def score_word(word: str, freqs: dict[str, float]) -> float:
    return sum([freqs[char] for char in set(word)])

def decorate_scorer(filename: str = "letter_freq.csv"):
    freqs = load_freqs(filename)

    def scorer(word: str):
        return score_word(word, freqs)
    
    return scorer