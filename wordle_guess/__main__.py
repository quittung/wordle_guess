"""command line interface that turns wordle hints into a list of possible words"""
import sys, argparse
from multiprocessing.pool import Pool

from app import guesser as gssr

def check_input(string, char_set):
    """checks if a string is 5 chars long and only contains chars from a given set"""
    return len(string) == 5 and not (set(string) - char_set)


if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "suggests words for wordle"
    parser.add_argument("-s", "--strategy", choices=["entropy", "commonwords", "commonletters", "commonswitch"], default="entropy", help="choose a strategy for sorting the candidates")
    args = parser.parse_args()


    # choose strategy
    if args.strategy == "entropy":
        pool = Pool()
        from app.strategies import entropy
        strategy = entropy.EntropyStrategy(pool)
    elif args.strategy == "commonwords": 
        from app.strategies import common_words
        strategy = common_words.CommonWordsStrategy()
    elif args.strategy == "commonletters": 
        from app.strategies import common_letters
        strategy = common_letters.CommonLettersStrategy()
    elif args.strategy == "commonswitch": 
        from app.strategies import common_switch
        strategy = common_switch.CommonSwitchStrategy()

    guesser = gssr.Guesser(strategy)

    # hints and explanations
    print("try '{}' first".format(guesser.candidates[0]))
    print("line by line, enter a word you tried")
    print("then enter the colors you got as g, y, b")
    print("")

    # start interactive loop
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
    
    if "pool" in locals(): pool.close()
