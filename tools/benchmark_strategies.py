import os, sys
from statistics import mean
from multiprocessing.pool import Pool

from tqdm import tqdm

# hacky import, but this is for development use only
sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 
from wordle_guess.app import guesser as gssr
from wordle_guess.app import wordle

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
    from wordle_guess.app.strategies import entropy
    pool = Pool()
    strategy = entropy.EntropyStrategy(pool)
    
    wordlist = gssr.load_wordlist()
    words = list(wordlist.keys())#[:100]
    words_num = len(words)

    # import cProfile
    # pr = cProfile.Profile()
    # pr.enable()

    scores = {} 

    for index, word in enumerate(tqdm(words)):
        score = run_game(word, gssr.Guesser(strategy, wordlist))
        scores[word] = score
        #print("{} -> {} ({} of {}, {:4.1f}%) ".format(word, score, index, words_num, index / words_num * 100))

    score_mean = mean(scores.values())
    print("strategy: {}".format(str(strategy)))
    print("average score: {}".format(score_mean))

    # pr.disable()
    # pr.print_stats()