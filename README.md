**Rugby League Predictor Game**

REQUIRED LIBRARIES:

- numpy
- shelve
- tkinter

This repo contains (among other things) a Python program that is a predictor game for Rugby League competitions.

This repo also contains pre-made league files (.dat/.dir) for some competitions that users may want to play the game with. There are files for the 2026 season of the Super League competition as well as the 2026, 2027 and 2028 seasons of the NRL based on the expected entry of Perth Bears into the competition in 2027 followed by Papua New Guinea Chiefs in 2028.

Features:

- Program interface is entirely a GUI
- Completely modifiable scoring system
- Team set creation system to allow for the game to be played with other competitions (i.e Super XIII, Queensland/NSW Cup, etc.)
- Derby fixture creation and management system to add detail to the previous feature
- Player management system that allows the user to add players to the game even when it is in progress
- Also keeps track of the league table including the feature where the loser of a game is awarded points if the margin of defeat is low enough (as in the Super XIII)

Long term TODO:

- Add a feature to break down per-round player scores
