# Roguelike Map Generator
Five python programs I made that quickly generates different roguelike style maps, some of which are inspired from popular roguelikes.

## Maps
- **Scroll:** Based on Slay the Spire. Generates a scroll that you traverse bottom-to-top, ending with a boss tile. You can control the spread of the map, as well as the number of nodes you have to traverse in order to go from bottom to top.

- **Grid:** Generates a large grid of squares with a key and a boss room. You can specify the minimum and maximum number of squares that could be present on the map.

- **Dungeon:** Generates a room-based system with connecting tiles that can have events inside of them. Includes a boss room as well as side paths that can sometimes connect back to the main path. You can control how long the main path can be, how many tiles should be used for side paths, and how long a side path can be.

- **Waypoints:** Based on Faster Than Light. Generates several tiles that are inter-connected based on distance. You can control how far the main path should go until the boss tile, as well as how many side tiles the map should generate.

- **Stations:** Based partially on Subterranauts' system. Generates several station that each have a "pool" of events that you can encounter in each station. Meant to be traversed from bottom-to-top, but unlike scroll, you can go sideways as well. You can define the length and spread of the map, similar to scrolls. You can also specify how many events there are in each station.

## Controls
Upon running any of the scripts, you'll be prompted to input a few parameters for the map. After this, a pygame window will open with the map. Use WASD to move around the map, and hold shift to move faster. Left click to highlight a tile, and use middle mouse click to blank out a while. Right click to remove any highlights or blanks a tile has. For ```stations.py```, you can also use I in order to see the elements in a station.

## Use and Contributions
If you want to use any of the map generation algorithms in your own game, feel free to do so. Furthermore if you want to contribute to the project by adding more map generation styles, or improve one of the map generation styles, feel free to do so.

For the full official license, see [the license document](LICENSE.md).