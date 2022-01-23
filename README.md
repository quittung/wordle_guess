# wordle_guess
A script to take the fun out of playing [Wordle](https://www.powerlanguage.co.uk/wordle/).


## Usage
Feed it the current hints and you will get the a word to try. Repeat until finding the solution. Usually takes 3 or 4 rounds to complete.

Use the script `wordle_prompt.py` for an interactive prompt. `wordle.py` contains all of the internal logic for filtering words. Sample output is below.

Because of type hinting, **Python 3.9 or higher is required**.


## Sample Output
```
try 'tears' first
line by line, enter a word you tried
then enter the colors you got as g, y, b

enter word:   tears
enter colors: bgbyb
1256 -> never
Alternatives: ['weren', 'mercy', 'fever', 'nerve', 'derek']

enter word:   never
enter colors: ggyyy
4 -> nerve
Alternatives: ['nervy', 'nervo', 'nervi']

enter word:   nerve
enter colors: ggggg
1 -> nerve
```
The solution was indeed "nerve".


## License and Attributions
The frequency ordered word list (en_opensubs.txt) is taken from [hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords), which is scraped from OpenSubtitles. License is "CC-by-sa-4.0".

The verified word list (en_letterpress.txt) is taken from [lorenbrichter/Words](https://github.com/lorenbrichter/Words), which is scraped from OpenSubtitles. License is "CC0-1.0 License".

words.txt is derived from the intersection of those two lists.

My code is licensed under the MIT License. 

Feel free to fork or do whatever. If I made a mistake attributing the word list or something else is wrong, please open an issue.
