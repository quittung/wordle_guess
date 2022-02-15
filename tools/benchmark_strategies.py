import os, sys
from statistics import mean
from multiprocessing.pool import Pool

from tqdm import tqdm

# hacky import, but this is for development use only
sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 
from wordle_guess.app import guesser as gssr
from wordle_guess.app import wordle
from wordle_guess.app.strategies import entropy, common_words, common_letters, common_switch

def run_game(solution, guesser: gssr.Guesser):
    round_counter = 1
    while round_counter < 7:
        guess = guesser.candidates[0]
        
        if guess == solution:
            break

        pattern = wordle.get_pattern(guess, solution)
        guesser.process_hint(guess, pattern)

        round_counter += 1
    
    return round_counter


if __name__ == "__main__":
    pool = Pool()
    strategies = [
        common_words.CommonWordsStrategy(),
        common_letters.CommonLettersStrategy(),
        common_switch.CommonSwitchStrategy(),
        entropy.EntropyStrategy(pool)
    ]
    
    wordlist = gssr.load_wordlist()
    words = list(wordlist.keys())[:1000]

    for strategy in strategies:
        scores = {} 

        for index, word in enumerate(tqdm(words)):
            score = run_game(word, gssr.Guesser(strategy, wordlist))
            scores[word] = score

        score_mean = mean(scores.values())
        print("strategy: {}".format(str(strategy)))
        print("average score: {:.2f}".format(score_mean))
        print("")