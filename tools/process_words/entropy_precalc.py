import sys, os.path
import json

# hacky import, but this is for development use only
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..")) 
from wordle_guess.modules import guesser
from wordle_guess.modules.strategies import entropy

print("loading list")
wordlist = guesser.load_wordlist()

print("calculating entropy")
print("this might take a while...")
entropy_dict = entropy.entropy_for_list(wordlist)

print("exporting list")
with open(os.path.join(os.path.dirname(__file__), "..", "..", "wordle_guess", "data", "entropy.json"), 'w', encoding="utf-8") as fobj:
    json.dump(entropy_dict, fobj, indent=2)