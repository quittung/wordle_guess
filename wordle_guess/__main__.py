"""command line interface that turns wordle hints into a list of possible words"""

from app import guesser as gssr
from app.strategies import entropy
from app.strategies import hints_then_common

import os

def check_input(string, char_set):
    """checks if a string is 5 chars long and only contains chars from a given set"""
    return len(string) == 5 and not (set(string) - char_set)


if __name__ == "__main__":
    guesser = gssr.Guesser(entropy.EntropyStrategy())
    #guesser = gssr.Guesser(unusual_then_common.UnusualThenCommonStrategy())

    # hints and explanations
    print("try '{}' first".format(guesser.candidates[0]))
    print("line by line, enter a word you tried")
    print("then enter the colors you got as g, y, b")
    print("")

    while True:
        # get user input
        word = input("enter word:   ")
        if not check_input(word, set("abcdefghijklmnopqrstuvwxyz")):  
            print("invalid input\n")
            continue
        
        pattern = input("enter colors: ")
        if not check_input(pattern, set("gyb")): 
            print("invalid input\n")
            continue
        
        # update data
        guesser.process_hint(word, pattern)

        # print candidates
        print("try this: {}".format(guesser.candidates[0]))
        if len(guesser.candidates) == 1: 
            input("no alternatives, press enter to exit")
            break
        else:
            print("{} alternative{}: {}".format(len(guesser.candidates) - 1, "s" if len(guesser.candidates) > 2 else "", guesser.candidates[1:6]))
            print("")
