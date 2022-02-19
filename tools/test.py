import collections
import os, sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 
from wordle_guess.app.strategies import entropy
from wordle_guess.app import wordle

class TestIntegration(unittest.TestCase):
    def test_entropy(self):
        test_data = [
            [["a", "b", "c", "d"], 2],
            [["a", "b", "a", "b"], 1],
            [["a", "a", "b", "b"], 1],
            [["a", "a", "a", "b"], 0.811],
        ]

        for challenge, expected_response in test_data:
            counted = entropy.normalize(collections.Counter(challenge))

            probability = counted.values()
            info = entropy.get_information(probability)
            response = entropy.get_entropy(probability, info)

            self.assertAlmostEqual(response, expected_response, places=3)

    
    def test_pattern(self):
        test_data = [
            [("bbba", "abcb"), "ygby"],
            [("bbba", "abcd"), "bgby"],
            [("abba", "abcd"), "ggbb"],
        ]

        for (guess, solution), expected_response in test_data:
            response = wordle.get_pattern(guess, solution)
            self.assertEqual(response, expected_response)


if __name__ == '__main__':  
    unittest.main()

    