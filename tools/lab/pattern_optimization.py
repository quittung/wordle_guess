import os, sys
import time
import cProfile

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

func_dict = {
    "original": get_pattern, 
    "enumerate": get_pattern_enumerate,
    "precise": get_pattern_precise,
    "quick": get_pattern_precise_quicker,
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