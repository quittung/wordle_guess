# wordle_guess
A script to take the fun out of playing [Wordle](https://www.powerlanguage.co.uk/wordle/).


## Sample Output
```
try 'atone' first
line by line, enter a word you tried
then enter the colors you got as g, y, b

enter word:   atone
enter colors: ybbbb
try this: hairs
1063 alternatives: ['raids', 'daris', 'dashi', 'sidha', 'liars']

enter word:   hairs
enter colors: yybgy
try this: sharp
3 alternatives: ['shark', 'shard', 'shura']

enter word:   sharp
enter colors: ggggb
try this: shark
1 alternative: ['shard']

enter word:   shark
enter colors: ggggb
try this: shard
no alternatives, press enter to exit
```
The solution was indeed "shard".


## Usage
Run the app using the command `python3 wordle_guess` to get an interactive prompt. Feed it the current hints and you will get the a word to try. Repeat until finding the solution. Usually takes 3 or 4 rounds to complete.

Because of type hinting, **Python 3.9 or higher is required**.

You can choose different strategies with the `-s` argument:

### Entropy (Standard)
```python3 wordle_guess -s entropy```

This strategy was inspired by [3Blue1Brown's video on wordle](https://www.youtube.com/watch?v=v68zYyaEmEA). For every remaining word (guess) it calculates its entropy using the following steps:
 - for every possible remaining solution, calculate the amount of information gained by using that guess 
 - calculate the average of that information, weighted by the likelyhood of that solution appearing in everyday speech
 Information is defined as the logarithm with base two of the number of possible words before guessing divided by the number after for that specific, assumed solution. In other words, it answers how many times a guess would cut the list of possible words in two.
 
Average score for the 1000 most common 5 letter words: 3.49
 
### Common Words
```python3 wordle_guess -s commonwords```

This strategy ranks the remaining words by how likely they are to apper in everyday speech.

Average score: 3.76

### Common Letters
```python3 wordle_guess -s commonletters```

This strategy ranks the remaining words by how common each word's letters are. The intuition here is that knowing about a more common letter will be a more valuable hint. 

Average score: 4.63

### Common Letters, Then Common Words
```python3 wordle_guess -s commonswitch```

This strategy focuses on getting hints first as long as the list of remaining words is longer than 119. After that it tries the most common word first. 
This strategy is based on how I play wordle without assistance. The threshold has been determined experimentally.

Average score: 3.53


## Links
Play wordle [here](https://www.powerlanguage.co.uk/wordle/). Try [this](https://hellowordl.net/) version without a daily limit.

## License and Attributions
The frequency ordered word list (en_opensubs.txt) is taken from [hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords), which is scraped from OpenSubtitles. License is "CC-by-sa-4.0".

The verified word list (en_letterpress.txt) is taken from [lorenbrichter/Words](https://github.com/lorenbrichter/Words), which is scraped from OpenSubtitles. License is "CC0-1.0 License".

words.txt is derived from the intersection of those two lists.

The frequency data of individual letters is taken from [this Cornell University site](http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html). As I (not a lawyer, not legal advice) understand it, this is a collection of facts, wich is not protected under copyright laws.

My code is licensed under the MIT License. 

Feel free to fork or do whatever. If I made a mistake attributing the word list or something else is wrong, please open an issue.
