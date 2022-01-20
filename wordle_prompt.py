from wordle import search, load_wordlist

def check_input(string, char_set):
    """checks if a string is 5 chars long and only contains chars from a given set"""
    return len(string) == 5 and not (set(string) - char_set)


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
        if colors[i] == "b":
            data["black"] += word[i]
        elif colors[i] == "y":
            if word[i] in data["yellow"]:
                data["yellow"][word[i]].append(i)
            else:
                data["yellow"][word[i]] = [i]
        elif colors[i] == "g":
            data["green"][word[i]] = i
    
    # run search
    candidates = search(wordlist, data)
    print("{} -> {}".format(len(candidates), candidates[0]))
    print("Alternatives: {}".format(candidates[1:min(6, len(candidates) - 1)]))
    print("")
