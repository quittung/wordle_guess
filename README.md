# wordle_guess
A script to take the fun out of playing [Wordle](https://www.powerlanguage.co.uk/wordle/).


## Usage
Feed it the current hints and you will get the a word to enter. Repeat until finding the solution usually takes 3 or 4 rounds to complete.

The main script is wordle.py. The data is entered as a python dictionary at around line 80, which is a bit clunky and could be improved. Sample data is already included.

Because of type hinting, **Python 3.9 or higher is required**.


## Sample Output
I tried "tears" first, despite the script suggesting right.
```
# of candidates -> best guess
99852 -> right
3163 -> wrong
51 -> drink
```
The solution was indeed "drink".


## License and Attributions
Word list (en_full.txt) is taken from [hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords), which is scraped from OpenSubtitles. words.txt is derived from that. License is CC-by-sa-4.0.

My code is licensed under the MIT License. 

Feel free to fork or do whatever. If I made a mistake attributing the word list or something else is wrong, please open an issue.
