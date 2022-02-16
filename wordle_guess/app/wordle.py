"""handles wordl hints and filtering wordlists accordingly"""

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



class WordleHint(object):
    """keeps track of wordle patterns"""
    def __init__(self) -> None:
        """creates empty hint"""
        self.black: set[str] = set()
        self.yellow: dict[str, set[int]] = {}
        self.green: dict[str, set[int]] = {}
    
    def _register_hint(self, color_dict: dict[str, set[int]], letter: str, index: int):
        """registers a green or yellow hint""" 
        if letter in color_dict:
            color_dict[letter].add(index)
        else:
            color_dict[letter] = set([index])

    def update_data(self, word: str, pattern: str):
        """updates data with new hint"""
        for i, color in enumerate(pattern):
                if color == "y":
                    self._register_hint(self.yellow, word[i], i)
                elif color == "g":
                    self._register_hint(self.green, word[i], i)
            
        for i, color in enumerate(pattern):
            if color == "b":
                # a character can be black if all other instances of it have been found
                if not (word[i] in self.yellow or word[i] in self.green): 
                    self.black.add(word[i])
                else:
                    self._register_hint(self.yellow, word[i], i)

def search(wordlist: dict[str, int], data: WordleHint):
    """searches for candidates and guesses for a given word list and data set"""
    candidates = filter_black(list(wordlist), data.black)
    for letter in data.yellow:
        candidates = filter_yellow(candidates, letter, data.yellow[letter])
    for letter in data.green:
        candidates = filter_green(candidates, letter, data.green[letter])

    return {word: wordlist[word] for word in candidates}


def get_pattern(guess: str, solution: str):
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