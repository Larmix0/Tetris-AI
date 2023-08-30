# What the project is about
This is a tetris game powered by an AI made in python using the pygame library.

This bot was made slowly over the months with small changes every now and then, therefore you shouldn't set your expectations too high in terms of how the code is since my decision making changed (and I'd say improved) over time, and my style also changed.
I'm still pretty proud about this project since the AI runs relatively fast (~0.15 seconds per move) despite calculating 1 move into the future.

# Playing the game
After running the game you use left arrow and right arrow to move the piece. Up arrow rotates, and control hard-drops the piece. Press spacebar during the game to toggle the AI on and off.

# Running the project
### To run the game/ai:

run.py file as a script <br>
or run the following command:
```
python -m run.py
```

### To run all tests:
```
python -m unittest discover tests
```

### To run a specific test (* is a wildcard for any tested file):
```
python -m unittest tests.test_*
```

<br>

# Note about the AI
**It's worth mentioning that the AI reading into the future only computes: current -> next and held piece -> next.** So it doesn't compute current -> held or held -> next (granted they're similar anyways). So there's no need to mention that missing about the AI. The reason that's the case is because it would take too much time and would barely help the AI at all especially since current -> held usually leads to the same positions as held -> current anyways.