"""A library that implements the Wordle game."""

import collections
import random


def eval_guess(target: str, guess: str) -> str:
    """Compare target and guess. Target and guess are both the same length.
    Return a string of the same length as target and guess,
    where a character encodes the match:
    - ! for a match
    - for a miss
    - + when the character appears in a different position.

    When evaluating if a character is a +, first remove the exact matches.

    >>> eval_guess('which', 'whisk')
    '!!!--'
    >>> eval_guess('which', 'which')
    '!!!!!'
    >>> eval_guess('which', 'guess')
    '-----'
    >>> eval_guess('eerie', 'where')
    '--++!'
    >>> eval_guess('where', 'eerie')
    '+-+-!'
    """
    # find the indices of characters that don't match the target
    wrong = [i for i, (t, g) in enumerate(zip(target, guess)) if t != g]
    # count character occurrences in target
    # at `wrong` positions using collections.Counter
    counts = collections.Counter(target[i] for i in wrong)

    # initialize result (list) with !
    result = ['!' for _ in target]

    # for each guessed character in wrong, replace result with +
    # if the characters count is more than 0, otherwise replace with -
    # decrease counts by 1 for each +
    for i in wrong:
        if counts[guess[i]] > 0:
            result[i] = '+'
            counts[guess[i]] -= 1
        else:
            result[i] = '-'

    return ''.join(result)

def eval_guess_test():
    """Test eval_guess()
    """
    assert eval_guess('which', 'whisk') == '!!!--'
    assert eval_guess('which', 'which') == '!!!!!'
    assert eval_guess('which', 'guess') == '-----'
    assert eval_guess('eerie', 'where') == '--++!'
    assert eval_guess('where', 'eerie') == '+-+-!'


class Wordlist:
    """Double wordlist.

    Loaded from a tsv file, two columns:
    - the word
    - 0/1 is in the smaller wordlist?

    The larger wordlist contains permissible guesses,
    the smaller one is a set of challenges.
    """

    def __init__(self, path):
        words, challenges = Wordlist.load(path)

        self.all = words
        self.all_set = set(words)
        self.challenges = challenges

    @staticmethod
    def load(filepath):
        """Load from tsv,

        Return a tuple where the first element is set of all words
        the second element is a list of words that have 1 in the second field.
        """
        with open(filepath) as f:
            fields = [line.strip().split('\t') for line in f]

        all_words = [word for word, _ in fields]
        one_in_second = [word for word, is_challenge in fields if is_challenge == '1']

        return all_words, one_in_second

    def in_dict(self, word):
        """Check if the word is in the wordlist.
        """
        return word in self.all_set

    def get_random_challenge(self):
        """Return a random challenge from the challenge list.
        """
        return random.choice(self.challenges)


# The original Wordle wordlist
# loaded as instance data
# FIXME: use importlib https://importlib-resources.readthedocs.io/en/latest/using.html#example
words = Wordlist('words.tsv')

class Game:
    """A single wordle game.
    """
    def __init__(self, word_index=None):
        """word_index is an index to words.challenges, use random word if None"""
        self.word = words.get_random_challenge() if word_index is None else words.challenges[word_index]

    def eval_guess(self, guess: str) -> str:
        """Evaluate the guess against selected word.

        First check if the guess is in the wordlist.
        Then evaluate the guess against the word.
        """
        if not words.in_dict(guess):
            return '-' * len(guess)

        return eval_guess(self.word, guess)
