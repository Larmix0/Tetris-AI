# What the project is about
This is a tetris game powered by an AI made in python using the pygame library. It's also dynamic in height and width (though the math isn't the most dynamic currently, so offsets do break if you change rows and cols too much in constants.py).

This bot was made slowly over the months with small changes every now and then, so you shouldn't set your expectations too high in terms of how the code is since my decision making changed (and I'd say improved) over time, and my style also changed.
I'm still pretty proud about this project since the AI runs relatively fast (~0.15 seconds per move) despite calculating 1 move into the future.

# Playing the game
After running the game you use left arrow and right arrow to move the piece. Up arrow rotates, down arrow moves down, control hard-drops the piece, and "z" holds the piece. Press "t" during the game to toggle the AI on and off.

# Running the project

1. Clone the project with `git clone https://github.com/Larmix0/Tetris-AI.git`

2. Change to project directory with `cd Tetris-AI`

3. Create and activate a virtual environment if you don't want to install packages directly on your global pip (look for a tutorial if you don't know how).

4. Install the required packages for the project with `pip install -r requirements.txt`

5. Run the run.py file as a script or type `python run.py`

# Running tests
### To run all tests:
```
python -m unittest discover tests
```

### To run a specific test (replace * with any valid test file's name):
```
python -m unittest tests.test_*
```

<br>

# Note about the AI
**It's worth mentioning that the AI reading into the future only computes: current -> next and held piece -> next.** So it doesn't compute current -> held or held -> next (granted they're similar anyways). So there's no need to mention that missing about the AI. The reason that's the case is because it would take too much time and would barely help the AI at all especially since current -> held usually leads to the same positions as held -> current anyways.
