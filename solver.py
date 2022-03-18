"""Wordle solver.
"""
import collections
import math
import pickle
import time
from typing import Optional
import random

import wordle


def filter(candidates: list[str], guess: str, pattern: str) -> list[str]:
    """Filter candidates by pattern.
    """
    return [word for word in candidates if wordle.eval_guess(word, guess) == pattern]

class RandomSolver:
    """Try to solve wordle game by random guessing.
    After each guess, filter the candidate list.
    """
    def __init__(self, game: wordle.Game):
        """Initialze candidates from challenges wordlist."""
        self.candidates = wordle.words.challenges
        self.game = game

    def solve(self, max_rounds=None, verbose=False) -> tuple[int, Optional[str]]:
        """Solve the game by random guessing. Take guesses from `wordle.words.all`.
        If there is only one candidate left, we're done.

        If max_rounds is set, limit the number of rounds.

        return (rounds, guess)
        """
        rounds = 0
        while True:
            guess = random.choice(wordle.words.all)
            pattern = self.game.eval_guess(guess)
            self.candidates = filter(self.candidates, guess, pattern)

            if verbose:
                print(f'{guess} -> {pattern} -> {len(self.candidates)}')

            rounds += 1
            if len(self.candidates) == 1:
                return rounds, self.candidates[0]

            if max_rounds is not None and rounds >= max_rounds:
                return rounds, None

def entropy_list(strings: list[str]) -> float:
    """Calculate the entropy of a list of strings.
    First count the strings using Counter.
    Then convert the counts to probabilities.
    Then calculate the entropy.
    """
    counter = collections.Counter(strings)
    counts = [count / len(strings) for count in counter.values()]

    return -sum(p * math.log(p, 2) for p in counts)

def entropies(guesses: list[str], targets: list[str]) -> list[tuple[float, str]]:
    """For each guess in guesses generate patterns
    by calling wordle.eval_guess with each of targets.
    Then calculate the entropy of the resulting list of patterns.

    Return a list of tuples (entropy, guess).
    """
    return [(entropy_list([wordle.eval_guess(target, guess) for target in targets]), guess) for guess in guesses]


class Timer:
    """Context manager to measure the time.
    """
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.elapsed = self.end - self.start


class EntropySolver:
    """Try to solve wordle game by maximizing entropy.
    """
    def __init__(self, game: wordle.Game):
        """Initialze candidates from challenges wordlist."""
        self.candidates = wordle.words.challenges
        self.game = game

        try:
            with open('soare.p', 'rb') as f:
                # (first_guess, memo_candidates, memo_guess)
                self.memo = pickle.load(f)
        except FileNotFoundError:
            self.memo = None


    def solve(self, max_rounds=None, verbose=False) -> tuple[int, Optional[str]]:
        """Solve the game by maximizing entropy. Take guesses from `wordle.words.all`.
        If there is only one candidate left, we're done.

        If max_rounds is set, limit the number of rounds.

        return (rounds, guess)
        """
        rounds = 0
        while True:
            guesses = wordle.words.all
            with Timer() as t:
                # if we got the pre-calculated data, use it
                if self.memo and rounds < 2:
                    if rounds == 0:
                        best_guess = self.memo[0]
                        pattern = self.game.eval_guess(best_guess[1])
                        self.candidates = self.memo[1][pattern]
                    elif rounds == 1:
                        # best guess depends on the first guess
                        pattern = self.game.eval_guess(self.memo[0][1])
                        best_guess = self.memo[2][pattern]
                        # here it's fall through to the normal loop
                else:
                    # to avoid getting stuck at the end, randomize the top within limits
                    top_guesses = sorted(entropies(guesses, self.candidates), reverse=True)

                    # pick all within 0.1 of the top entropy
                    max_ent = top_guesses[0][0]
                    for max_guess, (ent, _) in enumerate(top_guesses):
                        if ent < max_ent - 0.1:
                            break

                    # print(max_ent, max_guess, top_guesses[:10], top_guesses[max_guess - 1])

                    # pick a random guess from the top guesses
                    best_guess = random.choice(top_guesses[:max_guess])

                pattern = self.game.eval_guess(best_guess[1])
                self.candidates = filter(self.candidates, best_guess[1], pattern)

            if verbose:
                print(f'{t.elapsed:5.2f} {best_guess[1]} -> {pattern} -> {len(self.candidates)}')

            rounds += 1
            if len(self.candidates) == 1:
                return rounds, self.candidates[0]

            if max_rounds is not None and rounds >= max_rounds:
                return rounds, None