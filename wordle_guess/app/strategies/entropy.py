import collections
from functools import partial
import math
from multiprocessing.pool import Pool

from .. import loader
from ..wordle import get_pattern
from . import strategy



def dictmap(function, data: dict):
    """makes functions designed for lists work with dicts"""
    return dict(zip(data.keys(), function(data.values())))

def flexmap(func, data: list, pool: Pool = None, tracker = None):
    """mapper that works with and without multithreading"""
    if tracker:
        data = tracker(data)
    
    if pool == None:
        mapper = map
    else:
        if tracker:
            mapper = partial(pool.map, chunksize = 250)
        else:
            mapper = pool.map
    
    return list(mapper(func, data))


def normalize(values: list[float]) -> list[float]:
    total = sum(values)
    return [item / total for item in values]

def get_information(rel_freq_list: list[float]):
    """get the information from relative frequency for each list member"""
    return [-math.log2(rf) for rf in rel_freq_list]

def get_entropy(prob_list: list[float], info_list: list[float]):
    """get entropy from list of probability of events and their information"""
    return sum(p * i for p, i in zip(prob_list, info_list))


def entropy_for_guess(words: dict[str, float], guess: str):
    # get pattern and do basic stats
    pattern = {solution: get_pattern(guess, solution) for solution in words}

    # get information in bits describing how much a pattern narrows down the search space
    pattern_counted = dictmap(normalize, collections.Counter(pattern.values()))
    pattern_info = dictmap(get_information, pattern_counted)

    # get probability as sum of all word freqencies of a pattern
    pattern_prob = {pattern: 0.0 for pattern in pattern_counted}
    for solution, pattern in pattern.items():
        pattern_prob[pattern] += words[solution]

    # calculates entropy as sum of probability * information for each element
    return get_entropy(pattern_prob.values(), pattern_info.values())

def entropy_for_list(words_frequency: dict[str, float], pool: Pool = None, progress_tracker = None):
    words_frequency_normalized = dictmap(normalize, words_frequency)

    words = words_frequency.keys()
    words_entropy = dict(zip(words, flexmap(partial(entropy_for_guess, words_frequency_normalized), words, pool, progress_tracker)))

    words_entropy_sorted = dict(sorted(words_entropy.items(), key=lambda item: item[1], reverse=True))
    return words_entropy_sorted

class EntropyStrategy(strategy.Strategy):
    def sort_candidates(self, candidates: dict[str, int]) -> list[str]:
        return list(entropy_for_list(candidates, self.pool).keys())
    
    def sort_initial(self, candidates: dict[str, int]) -> list[str]:
        entropy_dict = loader.load_json("entropy.json")
        return list(entropy_dict.keys())