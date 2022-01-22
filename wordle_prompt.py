from wordle import search, load_wordlist

def check_input(string, char_set):
    """checks if a string is 5 chars long and only contains chars from a given set"""
    return len(string) == 5 and not (set(string) - char_set)

def register_hint(data, color, letter, index):
    """registers a green or yellow hint"""
    if letter in data[color]:
        data[color][letter].append(index)
    else:
        data[color][letter] = [index]



# preparing data
wordlist = load_wordlist()
data = {
    "black": "",
    "yellow": {
        
    },
    "green": {
        
    }
}

# hints and explanations
print("try 'tears' first")
print("line by line, enter a word you tried")
print("then enter the colors you got as g, y, b")
print("")

while True:
    # get user data
    word = input("enter word:   ")
    if not check_input(word, set("abcdefghijklmnopqrstuvwxyz")):  
        print("invalid input\n")
        continue
    
    colors = input("enter colors: ")
    if not check_input(colors, set("gyb")): 
        print("invalid input\n")
        continue
    
    # update data
    for i in range(5):
        if colors[i] == "y":
            register_hint(data, "yellow", word[i], i)
        elif colors[i] == "g":
            register_hint(data, "green", word[i], i)
    
    for i in range(5):
        if colors[i] == "b":
            # a character can be black if all other instances of it have been found
            if not (word[i] in data["yellow"] or word[i] in data["green"]): 
                data["black"] += word[i]
    
    # run search
    candidates = search(wordlist, data)
    print("{} -> {}".format(len(candidates), candidates[0]))

    if len(candidates) == 1:
        break

    print("Alternatives: {}".format(candidates[1:6]))
    print("")
