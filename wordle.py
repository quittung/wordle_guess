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

def filter_green(word_list, letter, indices: list[int]):
    """filters out words that don't have a given letter in a specified spot"""
    for index in indices:
        word_list = [word for word in word_list if word[index] == letter]
    return word_list

def load_wordlist(filename: str = "words.txt"):
    with open(filename, "r", encoding="utf-8") as fobj:
        words = fobj.readlines()
    words = [word[:-1] for word in words]
    return words


def search(wordlist: list[str], data: dict):
    """searches for candidates and guesses for a given word list and data set
 
    example of data to pass:
    {
        "black": "taswho",
        "yellow": {
            "e": [1, 4]
        },
        "green": {
            "r": 3
        }
    }
    """

    candidates = filter_black(wordlist.copy(), data["black"])

    data_yellow: dict[str, list[int]] = data["yellow"]
    for letter in data_yellow:
        candidates = filter_yellow(candidates, letter, data_yellow[letter])

    data_green: dict[str, int] = data["green"]
    for letter in data_green:
        candidates = filter_green(candidates, letter, data_green[letter])

    return candidates