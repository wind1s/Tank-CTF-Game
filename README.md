# Capture the Flag user manual

## Starting game

Start the game by running ```python3 ctf.py```. 
Add flag ```--singleplayer``` for singleplayer mode or ```--hot-multiplayer``` for 2-person multiplayer.
By default the game starts in singleplayer mode.

## Features

Singleplayer:
    Play alone vs AI.
    Control your tank using the arrow keys and shoot with spacebar.
Multiplayer:
    Play vs another player and AI.
    Player 1 moves with the arrow keys and shoots with spacebar.
    Player 2 moves with the WASD keys and shoots with X.

Map loader:
    Maps can be loaded from text files.

Hit Points:
    Tanks have 3HP by default, wood crates have 2HP.

Sound:
    WIP

Explosions:
    An explosion is displayed on bullet impact.

A* Search:
    AI uses A* pathfinding.

Improved AI:
    AI prioritizes paths without metal boxes and recalculates when stuck. 
    AI has an updated map with boxes in the right spot. AI also tries to intercept
    the path between player carrying flag and their base.

Unfair AI:
    When enabled, AI moves faster and is stronger.

Score Counting:
    Upon capturing flag, winning player gets a point and game restarts.
    
#### Future ideas

Game options, change key layout, ajust sound, cheat codes etc.
Add knockback to tanks.

## Files
cmdparser.py
    Reads flags when starting game

ctf.py
    Starts the game with flag arguments

ctfgame.py
    Class for entire game which creates holds all variables and game objects.
    Also runs game loop, which updates the game every frame.

keyevent.py
    Handles user keyboard input

collision.py
    Functions for collision handling

baseobject.py
    Base classes for game objects

gameobjects.py
    All game object classes used in the game

createobjects.py
    Function for creating new game objects

ai.py
    Class which controls AI tanks

maps.py
    Reads and loads maps from map files

images.py
    Loads image files to be used in game

sounds.py
    Loads sounds to be used in game

utility.py
    Useful functions such as mathematial operations and
    finding a specific tile