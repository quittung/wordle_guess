import os.path
import json
import collections
import math

from ..wordle import get_pattern
from . import strategy

def normalize(counts: dict[str, int]):
    counts_total = sum(counts.values())
    return {e: counts[e] / counts_total for e in counts}

def entropy_for_guess(guess: str, words_frequency_normalized: dict[str, float]):
    # get pattern and do basic stats
    solutions_pattern = {solution: get_pattern(guess, solution) for solution in words_frequency_normalized}
    patterns_incidence = collections.Counter(solutions_pattern.values())
    patterns_incidence_normalized = normalize(patterns_incidence)

    # get information in bits describing how much a pattern narrows down the search space
    patterns_information = {pattern: -math.log2(patterns_incidence_normalized[pattern]) for pattern in patterns_incidence_normalized}

    # get probability as sum of all word freqencies of a pattern
    patterns_probability_normalized = {pattern: 0.0 for pattern in patterns_incidence}
    for solution, pattern in solutions_pattern.items():
        patterns_probability_normalized[pattern] += words_frequency_normalized[solution]

    # calculates entropy as sum of probability * information for each element
    entropy = sum([a * b for a, b in zip(patterns_information.values(), patterns_probability_normalized.values())])
    return entropy

def entropy_for_list(words_frequency: dict[str, float]):
    words_frequency_normalized = normalize(words_frequency)
    words_entropy = {word: entropy_for_guess(word, words_frequency_normalized) for word in words_frequency}
    words_entropy_sorted = dict(sorted(words_entropy.items(), key=lambda item: item[1], reverse=True))
    return words_entropy_sorted

class EntropyStrategy(strategy.Strategy):
    def sort_candidates(self, candidates: dict[str, int]) -> list[str]:
        return list(entropy_for_list(candidates).keys())
    
    def sort_initial(self, candidates: dict[str, int]) -> list[str]:
        path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "entropy.json")
        with open(path, "r", encoding="utf-8") as fobj:
            entropy_dict = json.load(fobj)
        return list(entropy_dict.keys())