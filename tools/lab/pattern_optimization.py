from collections import Counter
import os, sys
import time
import cProfile
import functools

from tqdm import tqdm

# hacky import, but this is for development use only
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..")) 
from wordle_guess.app import guesser 


def get_pattern(guess, solution):
    """generates the patterns for a guess"""
    hint = ""
    for index in range(len(guess)):
        if not guess[index] in solution:
            hint += "b"
        else:
            if guess[index] == solution[index]:
                hint += "g"
            else:
                hint += "y"
    
    return hint

def get_pattern_enumerate(guess, solution):
    """generates the patterns for a guess"""
    hint = ""
    for index, letter in enumerate(guess):
        if not letter in solution:
            hint += "b"
        else:
            if letter == solution[index]:
                hint += "g"
            else:
                hint += "y"
    
    return hint

def get_pattern_precise(guess: str, solution: str):
    """generates the patterns for a guess"""
    hint = ""
    for index, letter in enumerate(guess):
        if not letter in solution:
            hint += "b"
        else:
            if letter == solution[index]:
                hint += "g"
            else:
                # only color yellow if not already marked in other yellow or any green
                letter_solution = solution.count(letter)
                letter_green = sum([l == letter and l == solution[i] for i, l in enumerate(guess)])
                letter_yellow_already = sum([l == letter and l != solution[i] for i, l in enumerate(guess[:index])])
                if letter_solution - letter_green - letter_yellow_already > 0:
                    hint += "y"
                else:
                    hint += "b"
    
    return hint

def get_pattern_precise_quicker(guess: str, solution: str):
    """generates the patterns for a guess"""
    hint = ""
    for index, letter in enumerate(guess):
        if not letter in solution:
            hint += "b"
        else:
            if letter == solution[index]:
                hint += "g"
            else:
                # only color yellow if not already marked in other yellow or any green
                letter_solution = solution.count(letter)
                letter_guess_already = guess[:index].count(letter)
                if letter_solution > letter_guess_already:
                    letter_green = sum([l == letter and l == solution[i] for i, l in enumerate(guess)])
                    if letter_solution > letter_guess_already + letter_green:
                        hint += "y"
                    else:
                        hint += "b"
                else:
                    hint += "b"

    return hint

def get_pattern_precise_different(guess: str, solution: str):
    """generates the patterns for a guess"""
    letter_budget = Counter(solution)
    hint = [None] * len(guess)

    for index, (letter_guess, letter_solution) in enumerate(zip(guess, solution)):
        if letter_guess == letter_solution:
            hint[index] = "g"
            letter_budget[letter_guess] -= 1
    
    for index, (letter_guess, letter_solution) in enumerate(zip(guess, solution)):
        if not letter_guess in letter_budget:
            hint[index] = "b"
        elif letter_guess != letter_solution:
            if letter_budget[letter_guess] > 0:
                hint[index] = "y"
                letter_budget[letter_guess] -= 1
            else:
                hint[index] = "b"

    return "".join(hint)

cached_counter_ext = functools.cache(Counter)

def get_pattern_precise_different_cached(guess: str, solution: str):
    """generates the patterns for a guess"""
    letter_budget = cached_counter_ext(solution)
    hint = [None] * len(guess)

    for index, (letter_guess, letter_solution) in enumerate(zip(guess, solution)):
        if letter_guess == letter_solution:
            hint[index] = "g"
            letter_budget[letter_guess] -= 1
    
    for index, (letter_guess, letter_solution) in enumerate(zip(guess, solution)):
        if not letter_guess in letter_budget:
            hint[index] = "b"
        elif letter_guess != letter_solution:
            if letter_budget[letter_guess] > 0:
                hint[index] = "y"
                letter_budget[letter_guess] -= 1
            else:
                hint[index] = "b"

    return "".join(hint)

def get_pattern_precise_different_inhouse(guess: str, solution: str):
    """generates the patterns for a guess"""
    letter_budget = {}
    for letter in solution:
        if letter in letter_budget:
            letter_budget[letter] += 1
        else:
            letter_budget[letter] = 1

    hint = [None] * len(guess)

    for index, (letter_guess, letter_solution) in enumerate(zip(guess, solution)):
        if letter_guess == letter_solution:
            hint[index] = "g"
            letter_budget[letter_guess] -= 1
    
    for index, (letter_guess, letter_solution) in enumerate(zip(guess, solution)):
        if not letter_guess in letter_budget:
            hint[index] = "b"
        elif letter_guess != letter_solution:
            if letter_budget[letter_guess] > 0:
                hint[index] = "y"
                letter_budget[letter_guess] -= 1
            else:
                hint[index] = "b"

    return "".join(hint)


@functools.cache
def cached_counter(solution):
    letter_budget = {}
    for letter in solution:
        if letter in letter_budget:
            letter_budget[letter] += 1
        else:
            letter_budget[letter] = 1
    return letter_budget

def get_pattern_precise_different_inhouse_cached(guess: str, solution: str):
    """generates the patterns for a guess"""
    letter_budget = cached_counter(solution)

    hint = [None] * len(guess)

    for index, (letter_guess, letter_solution) in enumerate(zip(guess, solution)):
        if letter_guess == letter_solution:
            hint[index] = "g"
            letter_budget[letter_guess] -= 1
    
    for index, (letter_guess, letter_solution) in enumerate(zip(guess, solution)):
        if not letter_guess in letter_budget:
            hint[index] = "b"
        elif letter_guess != letter_solution:
            if letter_budget[letter_guess] > 0:
                hint[index] = "y"
                letter_budget[letter_guess] -= 1
            else:
                hint[index] = "b"

    return "".join(hint)




#import pattern_cy  


word_list = list(guesser.load_wordlist().keys())[:2000]

# pattern_lookup = {}
# for guess in tqdm(word_list):
#         pattern_lookup[guess] = {solution: get_pattern_enumerate(guess, solution) for solution in word_list}


assert get_pattern_precise("bbba", "abcb") == "ygby"
assert get_pattern_precise("bbba", "abcd") == "bgby"
assert get_pattern_precise("abba", "abcd") == "ggbb"

assert get_pattern_precise_quicker("bbba", "abcb") == "ygby"
assert get_pattern_precise_quicker("bbba", "abcd") == "bgby"
assert get_pattern_precise_quicker("abba", "abcd") == "ggbb"

assert get_pattern_precise_different_inhouse("bbba", "abcb") == "ygby"
assert get_pattern_precise_different_inhouse("bbba", "abcd") == "bgby"
assert get_pattern_precise_different_inhouse("abba", "abcd") == "ggbb"

#assert pattern_cy.get_pattern_c("bbba", "abcb") == "ygby"
#assert pattern_cy.get_pattern_c("bbba", "abcd") == "bgby"
#assert pattern_cy.get_pattern_c("abba", "abcd") == "ggbb"

func_dict = {
    "original": get_pattern, 
    "enumerate": get_pattern_enumerate,
    "precise": get_pattern_precise,
    "quick": get_pattern_precise_quicker,
    "different": get_pattern_precise_different,
    "cached": get_pattern_precise_different_cached,
    "inhouse": get_pattern_precise_different_inhouse,
    "inhouse_c": get_pattern_precise_different_inhouse_cached,
#    "c": pattern_cy.get_pattern_c
    }
func_timing = {}

for func in func_dict:

    t_start = time.perf_counter()
    pr = cProfile.Profile()

    for guess in tqdm(word_list):
        pr.enable()
        for solution in word_list:
            func_dict[func](guess, solution)
        pr.disable()

    duration = time.perf_counter() - t_start
    pr.print_stats()
    func_timing[func] = duration
    print("{} -> {}".format(func, duration))

ref_time = func_timing["original"] #max(func_timing.values())
func_timing_rel = {func: (func_timing[func] / ref_time) - 1 for func in func_timing}
print(func_timing_rel)