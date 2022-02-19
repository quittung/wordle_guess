import collections
from functools import partial
import math
from multiprocessing.pool import Pool
from typing import Callable, Mapping, Iterable

from .. import loader
from ..wordle import get_pattern
from . import strategy



def optional_dict(function: Callable[[Iterable], Iterable]) -> Callable[[Mapping], dict]:
    """makes functions designed for lists work with dicts"""
    def inner(data):
        if isinstance(data, dict):
            return dict(zip(data.keys(), function(data.values())))
        else:
            return function(data)
    
    return inner

@optional_dict
def normalize(values: Iterable[float]) -> Iterable[float]:
    total = sum(values)
    return [item / total for item in values]

@optional_dict
def get_information(rel_freq_list: Iterable[float]):
    """get the information from relative frequency for each list member"""
    return [-math.log2(rf) for rf in rel_freq_list]

def get_entropy(prob_list: Iterable[float], info_list: Iterable[float]):
    """get entropy from list of probability of events and their information"""
    return sum(p * i for p, i in zip(prob_list, info_list))


def entropy_for_guess(words: Mapping[str, float], guess: str):
    # get pattern and do basic stats
    pattern = {solution: get_pattern(guess, solution) for solution in words}

    # get information in bits describing how much a pattern narrows down the search space
    pattern_counted = normalize(collections.Counter(pattern.values()))
    pattern_info = get_information(pattern_counted)

    # get probability as sum of all word freqencies of a pattern
    pattern_prob = {pattern: 0.0 for pattern in pattern_counted}
    for solution, pattern in pattern.items():
        pattern_prob[pattern] += words[solution]

    # calculate entropy
    return get_entropy(pattern_prob.values(), pattern_info.values())

def entropy_for_list(words_frequency: dict[str, float], mapper = map):
    # calculate relative frequency of the words
    words_rel_freq = normalize(words_frequency)

    # get entropy for all words
    words = words_frequency.keys()
    entropy = mapper(partial(entropy_for_guess, words_rel_freq), words)

    # package as dict and sort by entropy
    words_entropy = dict(zip(words, entropy))
    words_entropy_sorted = dict(sorted(words_entropy.items(), key=lambda item: item[1], reverse=True))

    return words_entropy_sorted

class EntropyStrategy(strategy.Strategy):
    def __init__(self, pool: Pool = None) -> None:        
        self.mapper = pool.map if pool else map

    def sort_candidates(self, candidates: dict[str, int]) -> list[str]:
        return list(entropy_for_list(candidates, self.mapper).keys())
    
    def sort_initial(self, candidates: dict[str, int]) -> list[str]:
        entropy_dict = loader.load_json("entropy.json")
        return list(entropy_dict.keys())