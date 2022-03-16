# Wordle solver in Python

Written mostly by GitHub Copilot.

The rest here is actually Copilot babble, trying to write a readme.

> A demonstration of a project written by Copilot. At least in part, this project is a wordle solver. When Copilot is not programming, he is playing a game called "Wordle". Let's try if he can solve it.

## How to use
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

# EntropySolver is used in similar manner
solver.EntropySolver(wordle.Game(word_index=1)).solve(verbose=True, max_rounds=6)
```

## Pre-computed first round
```
import wordle, solver
soare_patterns = set(wordle.eval_guess(c, 'soare') for c in wordle.words.challenges)
soare_cands = {pat:solver.filter(wordle.words.challenges, 'soare', pat) for pat in soare_patterns}
soare_guess = {pat:max(solver.entropies(wordle.words.all, cands), key=lambda x: x[0]) for pat, cands in soare_cands.items()}
second_cands = {pat:solver.filter(soare_cands[pat], wordle.eval_guess(), pat) for pat in soare_guess.keys()}
```
