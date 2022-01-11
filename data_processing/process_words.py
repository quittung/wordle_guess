# sanitizes the word list for faster use by the main script

with open("en_full.txt", 'r', encoding="utf-8") as fobj:
    words = fobj.readlines()

# throw away the fequency info
words = [word.split(" ")[0] for word in words]
# only keep five letter words
words = [word for word in words if len(word) == 5]
# only keep words made up of basic english letters
alpha = set("abcdefghijklmnopqrstuvwxyz")
words = [word for word in words if not (set(word) - alpha)]
# convert all words to lower case
words = [word.lower() for word in words]

with open("words.txt", 'w', encoding="utf-8") as fobj:
    fobj.writelines(word + "\n" for word in words)