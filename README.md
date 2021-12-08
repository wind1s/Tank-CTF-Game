## Capture the Flag User Manual
### Starting game
Start the game by running ```python3 ctf.py```. 
Press escape of click the window x to close the game.

Flag ```--game-mode```  + one of the following flags to choose game mode.
```singleplayer``` for singleplayer mode against ai's.
```hot-multiplayer``` for 2 player hot seat multiplayer mode against ai's.
By default the game starts in singleplayer mode.

To choose the map to play, use the flag ```--map``` and specify a map file from the map_files folder.
To display a help menu suppliy only the ```-h``` or ```--help``` flag.

### Easy features
##### Couting score:
The game continues indefinitely and keeps track of all players score.
The Scoreboard is printed each time a player wins the round. 

##### Sound:
WIP

##### Hot Seat Multiplayer:
Play vs another player and AI.
Player 1 moves with the arrow keys and shoots with spacebar.
Player 2 moves with the WASD keys and shoots with X.

##### Hit Points:
Tanks have 3HP by default, wood crates have 2HP.
Bullets do 1HP of damage.

##### Respawn protection:
Tanks have a respawn protection timer. Can't be Destroyed for 3 seconds.

##### Unfair AI:
AI moves faster and is stronger than human players.

### Medium features
##### Explosions:
An explosion is displayed on bullet impact.

##### Read maps from a text/json file:
Using the flag ```--map``` you can specify a ```.txt``` or ```.json``` file from the map_files directory.

### Hard features
##### A star search:
AI uses A* path finding instead of BFS when computing the shortest path to the flag/base.

##### AI Improvements:
AI currently reads a updated map each time when finding a new path.
The Flag is always dropped in the middle of a tile so the AI will can always pick it up.
AI now more easily can navigate around metal boxes (see custom feature Improved AI)

WIP: When another tank has the flag, the ai tries to intercept its path instead of going straight for the flag.

### Custom features
##### Bullet ricochet:
WIP

##### Improved AI:
To make the AI more human, the tolerance when turning och driving to a tile has a small random value added to it.
Sometimes the AI gets stuck against a bos. This is fixed by breaking the AI move cycle after a short period and trying again.


### Description of files
##### cmdparser.py
Reads flags when starting game

##### ctf.py
Starts the game with specified flags and loads the specified map.

##### ctfgame.py
The main game class which initializes all objects, sound, images, handlers etc.
Provides the game loop which updates the physics, screen, winning condtions and scoreboard.

##### keyaction.py
Initializes keyboard bindings and handles user keyboard input

##### eventhandler.py
Initializes the event handler which handles keyboard input and quit events.

##### collision.py
Collision handler class that initializes all collision handler logic.

##### baseobjects.py
Base classes for game objects

##### gameobjects.py
All game object classes used in the game.

##### createobjects.py
Functions for creating new game objects. Used to initialize the game.

##### ai.py
Class which controls AI tanks

##### maps.py
Defines the game map and provides functionality to read map files.

##### images.py
Loads images to be used in game as textures.

##### sounds.py
Loads sounds to be used in game.

##### utility.py
Useful functions such as mathematial operations and general functionality.

##### config.py
Contains configuration variables for the internal logic and some visible functionality such as player names and game start banner.