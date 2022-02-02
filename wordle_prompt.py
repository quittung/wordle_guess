from wordle import search, load_wordlist, WordleHint
from frequency import Scorer
import os

def check_input(string, char_set):
    """checks if a string is 5 chars long and only contains chars from a given set"""
    return len(string) == 5 and not (set(string) - char_set)


if __name__ == "__main__":
    # preparing data
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    wordlist = load_wordlist()
    scorer = Scorer()
    data = WordleHint()

    # hints and explanations
    starting_words = wordlist.copy()
    starting_words.sort(key=scorer, reverse=True)

    print("try '{}' first".format(starting_words[0]))
    print("line by line, enter a word you tried")
    print("then enter the colors you got as g, y, b")
    print("")

    while True:
        # get user input
        word = input("enter word:   ")
        if not check_input(word, set("abcdefghijklmnopqrstuvwxyz")):  
            print("invalid input\n")
            continue
        
        colors = input("enter colors: ")
        if not check_input(colors, set("gyb")): 
            print("invalid input\n")
            continue
        
        # update data
        data.update_data(word, colors)
                
        # run search
        candidates = search(wordlist, data)
        # focus on getting hints first by choosing words with common and unique letters
        if len(candidates) > 119: # optimized value for 2000 most common five letter words
            candidates.sort(key=scorer, reverse=True)

        # print candidates
        print("{} -> {}".format(len(candidates), candidates[0]))
        if len(candidates) == 1: 
            input("finished, press enter to exit")
            break
        print("Alternatives: {}".format(candidates[1:6]))
        print("")
