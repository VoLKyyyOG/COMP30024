# Guide to Part B Folders

## Motivations
Since we wanted to test many different games before we attack Chexers,
and with many different algorithms, we wanted a code structure that:
1. Allowed you to code algorithmic approaches independent to any game (coding to an interface)
2. Allowed easy one-hit coding for any game that coheres with the above (implementing the interface)
3. Was consistent

## How to Run a Game
To run any game, the following files/structure is necessary:
> common/mechanics.py          # fully defines two core objects of any game:
> common/referee               # Includes CUSTOM referee files that work with any game
> common/player                # Folder for any number of players to use for game
    > \_\_init\_\_.py   # Make it a package
    > generic_1         # Folder
      > __init__.py     # See Player_example for code
      > player.py       # See Player_example: implements \_\_init\_\_, update and action
    > generic_2 etc...

Execute from "`.../common`": `python -m referee [-flags] player/generic_1 player/generic_2` ... `player/generic_N` (N as appropriate)

The idea is to copy everything in "Base for Any Game" into a new folder
each time you want a new game *(see below)*

## Library breakdown

### Base for Any Game (BAG)
The idea is that every game has `game-mechanics` and a `Agent_Core`, as well as a `game_visualisation` scheme. If you can define the first two, you can run the game. The third is only necessary if you want to visualise it.

This folder contains the framework for these files: core methods and imports
are already within. So, every time you want a new game to be simulated:
1. Copy everything in "Base for Any Game" into a new Folder
2. Implement EVERY function in these files
3. ????
4. Profit

### Agents
Minimum dependencies: `Agent_Core`, `game-mechanics`

This contains the concrete implementations (with appropriate Codename) of any Agent subclass.
- Any new Agent should inherit from the Agent class (defined in `Agent_Core`)
- init, update and action MUST be implemented for any concrete Agent
- Note a lot of Agents will just 'wrap' some algorithm, e.g. `Agent_Minimax` is quite succinct

### Algorithms
I wanted a place to store implementation-indepenent, `Agent_Core`/`game-mechanics` dependent python code for any useful algorithm.
- `Node` is a refactoring of the Node class from Part A, except this will work with any `game-mechanics`
- `Minimax` has a refactoring of your code Akira
