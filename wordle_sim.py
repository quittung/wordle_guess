"""tries to determine the optimal point for switching strategies"""

from statistics import mean
from random import choices
from wordle import WordleHint, search, load_wordlist
from frequency import Scorer
from numpy import linspace
import multiprocessing as mp

def generate_hint(guess, solution):
    """generates the hint colors for a guess"""
    hint = ""
    for index in range(len(guess)):
        if not guess[index] in solution:
            hint += "b"
        else:
            if guess[index] == solution[index]:
                hint += "g"
            else:
                hint += "y"
    
    return hint


class Sim(object):
    def __init__(self, wordlist, scorer, switch_thresh, verbose = False):
        self.wordlist =  wordlist
        self.scorer = scorer
        self.switch_thresh = switch_thresh
        self.verbose = verbose

    def __call__(self, solution):
        if self.verbose:
            print("solution: {}".format(solution))

        # prepare data
        data = WordleHint()
        guess = ""
        round_counter = 0

        while guess != solution:
            # run search
            candidates = search(self.wordlist, data)
            # focus on getting hints first by choosing words with common and unique letters
            if len(candidates) > self.switch_thresh:
                candidates.sort(key=self.scorer, reverse=True)

            # process best guess
            guess = candidates[0]
            hint = generate_hint(guess, solution)
            data.update_data(guess, hint)

            # cleanup
            if self.verbose:
                print("")
                print("candidates: {}".format(len(candidates)))
                print("guess: {}".format(candidates[0]))
                print("hint:  {}".format(hint))
            
            round_counter += 1

        return round_counter

if __name__ == "__main__":
    # preparing data
    wordlist = load_wordlist()
    scorer = Scorer()

    print("choosing test data")
    test_words = wordlist[:2000]
    #test_words = choices(test_words, k=int(len(test_words) * 0.8))
    print("running simulation with {} samples".format(len(test_words)))

    center = 200
    width = center

    pool = mp.Pool()
    sim_cache = {}

    while width > 1:
        t_values = linspace(max(center - width, 0), center + width, 5)
        print(t_values)
        print("width: {}".format(width))
        duration = []
        for thresh in t_values:
            if thresh in sim_cache:
                duration_mean = sim_cache[thresh]
            else:
                sim = Sim(wordlist, scorer, thresh)            
                sim_log = pool.map(sim, test_words)
                duration_mean = mean(sim_log)
                sim_cache[thresh] = duration_mean
            duration.append(duration_mean)
            print("average duration:  {:.3f} rounds for t={:.1f}".format(duration_mean, thresh))

        center = t_values[duration.index(min(duration))]
        print("lowest: {}\n".format(center))

        width = width / 2


