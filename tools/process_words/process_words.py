# sanitizes the word list for faster use by the main script
import json
from os.path import join, dirname

def clean_list(list: list[str]):
    # only keep five letter words
    list = [word for word in list if len(word) == 5]
    # only keep words made up of basic english letters
    alpha = set("abcdefghijklmnopqrstuvwxyz")
    list = [word for word in list if not (set(word) - alpha)]
    # convert all words to lower case
    list = [word.lower() for word in list]
    
    return list


# read lists
print("reading lists")
with open(join(dirname(__file__), "en_opensubs.txt"), 'r', encoding="utf-8") as fobj:
    words_ordered = fobj.read().splitlines()
with open(join(dirname(__file__), "en_letterpress.txt"), 'r', encoding="utf-8") as fobj:
    words_cleaned = fobj.read().splitlines()


# do file specific cleanup
print("cleaning lists")
words_frequency = dict(word.split(" ") for word in words_ordered)
words_ordered = list(words_frequency.keys())

# clean lists
words_ordered = clean_list(words_ordered)
words_cleaned = clean_list(words_cleaned)


# verify ordered list with cleaned list
print("preparing lists")
words_cleaned_set = set(words_cleaned)
print("comparing lists")
words_ordered = [word for word in words_ordered if word in words_cleaned_set]

words_ordered_frequency = {word: int(words_frequency[word]) for word in words_ordered}

# write list to file
print("exporting list")
with open(join(dirname(__file__), "..", "..", "wordle_guess", "app", "data", "words.json"), 'w', encoding="utf-8") as fobj:
    json.dump(words_ordered_frequency, fobj, indent=2)

print("done")
print("remember to update the entropy list as well")