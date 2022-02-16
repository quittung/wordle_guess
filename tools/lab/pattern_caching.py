import cProfile
import functools
from multiprocessing.pool import Pool
import os, sys
from subprocess import call
import json, pickle
import time
import zlib
from matplotlib.font_manager import json_dump
import itertools

from tqdm import tqdm

# hacky import, but this is for development use only
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..")) 
from wordle_guess.app import guesser
from wordle_guess.app.wordle import get_pattern



        
def compress(obj):
    return zlib.compress(pickle.dumps(obj))

def decompress(obj):
    return pickle.loads(zlib.decompress(obj))



class SimpleFastPattern(object):
    def __init__(self) -> None:
        self.pattern_lookup = {}

    def __call__(self, guess, solution) -> str:
        key = "".join([guess, solution])
        if key in self.pattern_lookup:
            return self.pattern_lookup[key]
        else:
            pattern = get_pattern(guess, solution)
            self.pattern_lookup[key] = pattern
            return pattern

class FastPattern(object):
    def __init__(self, precalculate: list[str] = None, pool: Pool = None) -> None:
        self.pattern_lookup = {} 

        if precalculate:
            self.precalc_list = list(itertools.product(precalculate, repeat=2))

            if pool:
                pool.starmap_async(get_pattern, self.precalc_list, callback=self._apply_precalc)
            else:
                self.pattern_lookup = {"".join(words): get_pattern(words[0], words[1]) for words in self.precalc_list}
                self.precalc_list = None 

    def _apply_precalc(self, result):
        keys = ["".join(x) for x in self.precalc_list]
        for key, pattern in zip(keys, result):
            self.pattern_lookup[key] = pattern
        self.precalc_list = None

    def __call__(self, guess, solution) -> str:
        key = "".join([guess, solution])
        if key in self.pattern_lookup:
            return self.pattern_lookup[key]
        else:
            pattern = get_pattern(guess, solution)
            self.pattern_lookup[key] = pattern
            return pattern

class FastCompactPattern(object):
    def __init__(self, precalculate: list[str] = None, pool: Pool = None) -> None:
        self.pattern_lookup = {} 

        self.pattern_list = ["".join(pattern) for pattern in itertools.product(["b", "y", "g"], repeat=5)]
        self.pattern_dict = {p: n for n, p in enumerate(self.pattern_list)}

        if precalculate:
            self.precalc_list = list(itertools.product(precalculate, repeat=2))

            if pool:
                pool.starmap_async(get_pattern, self.precalc_list, callback=self._apply_precalc)
            else:
                self.pattern_lookup = {"".join(words): self.pattern_dict[get_pattern(words[0], words[1])] for words in self.precalc_list}
                self.precalc_list = None 

    def _apply_precalc(self, result):
        keys = ["".join(x) for x in self.precalc_list]
        for key, pattern in zip(keys, result):
            self.pattern_lookup[key] = self.pattern_dict[pattern]
        self.precalc_list = None

    def __call__(self, guess, solution) -> str:
        key = "".join([guess, solution])
        if key in self.pattern_lookup:
            return self.pattern_list[self.pattern_lookup[key]]
        else:
            pattern = get_pattern(guess, solution)
            self.pattern_lookup[key] = self.pattern_dict[pattern]
            return pattern

if __name__ == "__main__":
    word_list = list(guesser.load_wordlist().keys())#[:200]
    word_list_test = word_list[:2000]
    pool = Pool()

    func_dict = {
        "original": get_pattern, 
#        "lru1k": functools.cache(get_pattern),
        "cached": SimpleFastPattern(),
#        "precalculated": FastPattern(word_list_test[:1000], pool),
        "compressed": FastCompactPattern(),
    }


    for _ in range(2):
        func_timing = {}

        for func in func_dict:
            t_start = time.perf_counter()

            for guess in tqdm(word_list_test):
                for solution in word_list_test:
                    func_dict[func](guess, solution)

            duration = time.perf_counter() - t_start
            func_timing[func] = duration
            print("{} -> {:.3f}, sample: {}".format(func, duration, func_dict[func](guess, solution)))

        ref_time = func_timing["original"] #max(func_timing.values())
        func_timing_rel = {func: (func_timing[func] / ref_time) - 1 for func in func_timing}
        print(func_timing_rel)

    # for func in func_dict:
    #     size = len(compress(func_dict[func]))
    #     print("{} -> {}".format(func, size))
    #     print("{} -> {}".format(func, sys.getsizeof(func_dict[func])))


    # with open(os.path.join(os.path.dirname(__file__), "pattern_cache.pkl"), "wb") as fobj:
    #     fobj.write(compress(pattern_lookup))
