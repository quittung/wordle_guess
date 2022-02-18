import collections
import os, shutil, sys
import unittest
import filecmp
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 
from wordle_guess.app.strategies import entropy

class TestIntegration(unittest.TestCase):
    def test_entropy_equal(self):
        test_data = [
            [["a", "b", "c", "d"], 2],
            [["a", "b", "a", "b"], 1],
            [["a", "a", "b", "b"], 1],
            [["a", "a", "a", "b"], 0.811],
        ]

        for challenge, expected_response in test_data:
            counted = entropy.dictmap(entropy.normalize, collections.Counter(challenge))

            probability = counted.values()
            info = entropy.get_information(probability)
            response = entropy.get_entropy(probability, info)

            self.assertAlmostEqual(response, expected_response, places=3)


    # def test_sync_build(self):
    #     """test sync process with built executable
    #     FAILS IN DEBUG BUT RUNS FINE AS NORMAL TEST"""

    #     # build app
    #     set_cwd()
    #     os.chdir("..")
    #     subprocess.call(["python3", "build.py"])
    #     os.chdir("test")

    #     self.run_full_sync(TestVarsFullProcess(prefix=["python3", "../dist/gapsync"]), subprocess.call)


if __name__ == '__main__':  
    unittest.main()

    