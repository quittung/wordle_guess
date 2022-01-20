def filter_black(word_list: list[str], black_list: str):
    """filters out words containing one of the given letters"""
    for letter in black_list:
        word_list = [word for word in word_list if not letter in word]
    return word_list

def filter_yellow(word_list: list[str], letter: str, bad_indices: list[int]):
    """filters out words that don't contain the given letter or have it in the wrong spot"""
    word_list = [word for word in word_list if letter in word]
    for bad_index in bad_indices:
        word_list = [word for word in word_list if word[bad_index] != letter]
    return word_list

def filter_green(word_list, letter, index):
    """filters out words that don't have a given letter in a specified spot"""
    return [word for word in word_list if word[index] == letter]

def search(word_list: list[str], data: dict):
    """searches for candidates and guesses for a given word list and data set"""
    candidates = filter_black(word_list.copy(), data["black"])

    data_yellow: dict[str, list[int]] = data["yellow"]
    for letter in data_yellow:
        candidates = filter_yellow(candidates, letter, data_yellow[letter])

    data_green: dict[str, int] = data["green"]
    for letter in data_green:
        candidates = filter_green(candidates, letter, data_green[letter])

    return candidates




# read words and remove newline letter
with open("words.txt", 'r', encoding="utf-8") as fobj:
    words = fobj.readlines()
words = [word[:-1] for word in words]


""" 
vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
enter your data here <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
format: 
  black:  all wrong letters
  yellow: dict of yellow letters and all known bad indices in a list
  green:  dict of all green letters and the corresponding index
example:
{
    "black": "taswho",
    "yellow": {
        "e": [1, 4]
    },
    "green": {
        "r": 3
    }
}

data_list can contain multiple dictionaries
try tears first to cover a bunch of common letters
"""

data_list = [
    {
    "black": "",
    "yellow": {
        
    },
    "green": {
        
    }
},{
    "black": "tas",
    "yellow": {
        "r": [3]
    },
    "green": {
        "e": 1
    }
},{
    "black": "tas",
    "yellow": {
        "r": [3, 4],
        "v": [2],
        "e": [3]
    },
    "green": {
        "e": 1,
        "n": 0
    }
}]
# solution for test data was nerve


print("try starting with 'tears'")
print("# of candidates -> best guess")
for data in data_list:
    search_candidates = search(words, data)
    print("{} -> {}".format(len(search_candidates), search_candidates[0]))

print("Alternatives: {}".format(search_candidates[1:min(6, len(search_candidates) - 1)]))