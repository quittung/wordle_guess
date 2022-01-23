# sanitizes the word list for faster use by the main script

def clean_list(list):
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
with open("en_opensubs.txt", 'r', encoding="utf-8") as fobj:
    words_ordered = fobj.read().splitlines()
with open("en_letterpress.txt", 'r', encoding="utf-8") as fobj:
    words_cleaned = fobj.read().splitlines()


# do file specific cleanup
print("cleaning lists")
# throw away the fequency info
words_ordered = [word.split(" ")[0] for word in words_ordered]

# clean lists
words_ordered = clean_list(words_ordered)
words_cleaned = clean_list(words_cleaned)


# verify ordered list with cleaned list
print("preparing lists")
words_cleaned_set = set(words_cleaned)
print("comparing lists")
words_ordered = [word for word in words_ordered if word in words_cleaned_set]

# write list to file
print("exporting lists")
with open("words.txt", 'w', encoding="utf-8") as fobj:
    fobj.writelines(word + "\n" for word in words_ordered)