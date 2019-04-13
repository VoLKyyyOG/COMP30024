# Guide to Part B Folders

## Motivations
Since we wanted to test many different games before we attack Chexers,
and with many different algorithms, we wanted a code structure that:
1. Allowed you to code algorithmic approaches independent to any game (coding to an interface)
2. Allowed easy one-hit coding for any game that coheres with the above (implementing the interface)
3. Was consistent

## How to Run a Game
To run any game, the following files/structure is necessary:
> ./mechanics.py        # fully defines a ton of functions

> ./referee/            # Includes CUSTOM referee files that work with any game

> ./player/             # Folder for any number of players to use for game

    > \_\_init\_\_.py   # Make it a package. Blank file

    > generic_1/        # Folder

        > __init__.py   # See Player_example for code

        > player.py     # See Player_example - implements \_\_init\_\_, update and action

    > generic_2/

    > etc...

Execute from '.' scope:

> `python -m referee [-flags] player/generic_1 player/generic_2` ... `player/generic_N` (N as appropriate)

To implement a new game:
1. Copy `Base for Any Game` and rename it whatever
2. Fully define all variables/functions as indicated in `mechanics.py`
3. Fully define (at least one) players in 'players' by:
    - Make a copy of `example` scaffolding in `players` directory
    - Rename folder, as well as the Class in `player.py` and the import in `__init__.py`
    - Using `mechanics` functionality, or otherwise, define the core methods of this `player`
    - Dones

## Algorithm Storage
I wanted a place to store implementation-indepenent python code for any useful algorithm.
- `node` is a refactoring of the Node class from Part A, except this will work with any `mechanics`
- `minimax` has a refactoring of the TTT code for a 2-player minimax, and the associated `evaluation`

## Warnings
1. Annoyingly the referee jumps between using 'r', 'red' and 'Red' player flagging. It would be GREAT to fix this in future, but for now just recognise that 'colour' usually refers to either a single character code 'r' or the full name 'red'. This is reflected in `mechanics` - there is space to define NAMES and CODES for a game.
2. I thought that creating dozens of interfaces, and then documents to implement them would be frustrating, so the principle of 'copy-paste templates' is used above. For sake of version control, any 'important' modifications to any `referee` (or less importantly `player` documents) needs to be manually copied to the Base and any other games.
