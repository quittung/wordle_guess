# wordle_guess
A script to take the fun out of playing [Wordle](https://www.powerlanguage.co.uk/wordle/).


## Usage
Use the script `wordle_prompt.py` for an interactive prompt. Feed it the current hints and you will get the a word to try. Repeat until finding the solution. Usually takes 3 or 4 rounds to complete.

With more than 119 possible words, the script will focus on gathering hints and suggest words with more common letters. Below that it will order words by their frequency in everyday conversation.

Sample output is below.

Because of type hinting, **Python 3.9 or higher is required**.


## Sample Output
```
try 'atone' first
line by line, enter a word you tried
then enter the colors you got as g, y, b

enter word:   atone
enter colors: bbbby
956 -> heirs
Alternatives: ['hires', 'shier', 'rides', 'dries', 'sired']       

enter word:   heirs
enter colors: bgbyb
46 -> mercy
Alternatives: ['fever', 'rebel', 'reply', 'refer', 'fewer']       

enter word:   mercy
enter colors: bggbg
6 -> derby
Alternatives: ['jerky', 'perky', 'pervy', 'perdy', 'ferly']       

enter word:   derby
enter colors: ggggg
1 -> derby
```
The solution was indeed "derby".


## License and Attributions
The frequency ordered word list (en_opensubs.txt) is taken from [hermitdave/FrequencyWords](https://github.com/hermitdave/FrequencyWords), which is scraped from OpenSubtitles. License is "CC-by-sa-4.0".

The verified word list (en_letterpress.txt) is taken from [lorenbrichter/Words](https://github.com/lorenbrichter/Words), which is scraped from OpenSubtitles. License is "CC0-1.0 License".

words.txt is derived from the intersection of those two lists.

The frequency data of individual letters is taken from [this Cornell University site](http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/frequencies.html). As I (not a lawyer, not legal advice) understand it, this is a collection of facts, wich is not protected under copyright laws.

My code is licensed under the MIT License. 

Feel free to fork or do whatever. If I made a mistake attributing the word list or something else is wrong, please open an issue.
