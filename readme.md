# Wordle solver in Python

Written mostly by GitHub Copilot.

The rest here is actually Copilot babble, trying to write a readme.

> A demonstration of a project written by Copilot. At least in part, this project is a wordle solver. When Copilot is not programming, he is playing a game called "Wordle". Let's try if he can solve it.

## Slides

[Google Slides](https://docs.google.com/presentation/d/1-CfTiwKeEBTSmBw0XOjhKEt5Ml5vTGjlGLExq6Od1gw/edit#slide=id.p)

## How to use

Python 3.10

```
import wordle
import solver

solver.RandomSolver(wordle.Game(word_index=1)).solve(verbose=True)

# solve all challenges, calculate percentage solved
run = [
  solver.RandomSolver(wordle.Game(word_index=i)).solve(max_rounds=6)
  for i in range(len(wordle.words.challenges))
]
sum(1 for rounds, _ in run if rounds < 6) / len(wordle.words.challenges)

# 54% of challenges solved

# EntropySolver is used in similar manner
solver.EntropySolver(wordle.Game(word_index=1)).solve(verbose=True, max_rounds=6)
run = [
  solver.EntropySolver(wordle.Game(word_index=i)).solve(max_rounds=6)
  for i in range(len(wordle.words.challenges))
]
sum(1 for rounds, _ in run if rounds < 6) / len(wordle.words.challenges)
# 100% of challenges solved

import statistics
statistics.mean(r+1 for r, _ in run)
# 3.639
```

## Pre-computed first round
At start there are no clues. `soare` is the word that is picked every time by
the EntropySolver. We can also pre-compute the candidates based on pattern after
the first guess and the best guess for those candidates.

```
import wordle, solver
soare_patterns = set(wordle.eval_guess(c, 'soare') for c in wordle.words.challenges)
soare_cands = {pat:solver.filter(wordle.words.challenges, 'soare', pat) for pat in soare_patterns}
soare_guess = {pat:max(solver.entropies(wordle.words.all, cands), key=lambda x: x[0]) for pat, cands in soare_cands.items()}

with open('soare.p', 'wb') as fo:
    pickle.dump(((0, 'soare'), soare_cands, soare_guess), fo, protocol=pickle.HIGHEST_PROTOCOL)
```
