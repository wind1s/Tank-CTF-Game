## Tank CTF Game
### Starting game
Start the game by running ```python3 ctf.py```. 
Press escape of click the window x to close the game.

Flag ```--game-mode```  + one of the following flags to choose game mode.
```singleplayer``` for singleplayer mode against ai's.
```hot-multiplayer``` for 2 player hot seat multiplayer mode against ai's.
By default the game starts in singleplayer mode.
Choose AI difficulty with the flag ```--difficulty```.

To display a help menu suppliy only the ```-h``` or ```--help``` flag.

### Choosing map
To choose the map to play, use the flag ```--map``` and specify a map file from the map_files folder.
The file formats available are json and txt. 
##### JSON map format description
JSON map files are defined by 3 keys, "boxes", "start_positions" and "flag_position". "boxes" and "start_positions" is a 2D array
containing coordinates of the all boxes (including grass tiles) respectively the start positions of tanks. "flag_position" is a coordinate array for the flags position on the map.
##### TXT map format description
TXT map files are defined by 3 headers, "boxes", "start_positions" and "flag_position". Each row is separated by a newline ("\n").
Each row contains either a header marking the beginning of header data or a array defined by values separated by commas (",").
The "boxes" header rows define corresponding map row box positions (including grass tiles). "start_positions" header rows contain the coordinates of each tanks starting coordinate. "flag_position" header contains a single row marking the flags coordinate on the map.
