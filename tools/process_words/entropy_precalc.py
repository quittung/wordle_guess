import sys, os.path
import json
from multiprocessing.pool import Pool

from tqdm import tqdm

# hacky import, but this is for development use only
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..")) 
from wordle_guess.app import guesser
from wordle_guess.app.strategies import entropy

if __name__ == "__main__":
    print("loading list")
    wordlist = guesser.load_wordlist()

    print("calculating entropy")
    print("this might take a while...")
    entropy_dict = entropy.entropy_for_list(wordlist, Pool(), progress_tracker=tqdm)

    print("exporting list")
    with open(os.path.join(os.path.dirname(__file__), "..", "..", "wordle_guess", "app", "data", "entropy.json"), 'w', encoding="utf-8") as fobj:
        json.dump(entropy_dict, fobj, indent=2)