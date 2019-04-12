# Guide to Part B Folders

# Notes to self (Callum)
- I suspect the specification will eradicate the need for a common Agent_Core, as the
code will be so simple that there isn't a point being so convoluted.
- Ensure that the 'actions' the s_referee provides are converted to Action()
- Come back here and re-discuss execution, how referee will EASILY pull any agents needed
- Where will memory/time checks go (assuming referee doesn't have them)

## Motivations
Since we wanted to test many different games before we attack Chexers,
and with many different algorithms, we wanted a code structure that:
1. Allowed you to code algorithmic approaches independent to any game (coding to an interface)
2. Allowed easy one-hit coding for any game that coheres with the above (implementing the interface)
3. Was consistent

## How to Run a Game
To run a game, all of the following need to be in the same directory:
- `game_mechanics` fully defines two core objects of any game:
> Action (can capture any possible action made)
> State (can capture any possible game state as well as )

- `Agent_Core` is a (hopefully redundant) wrapping class that all agents inherit
    - Contains the Agent superclass that enforces init, update and action

- `referee` is the main function
- Any Concrete, game-implemented `Agent_generic.py` you want
> - `Agent_Terminal` reads input from command line (this is human player)
> - `Agent_File` replicates input from a file. This could facilitate 'replays'
> - `Agent_MC` will one day exist and implement a Monte-Carlo decision process
> - Etc.

Then execution is as easy as the specification specifies.

The idea is to copy everything in "Base for Any Game" into a new folder
each time you want a new game *(see below)*

## Library breakdown

### Base for Any Game (BAG)
The idea is that every game has `game_mechanics` and a `Agent_Core`, as well as a `game_visualisation` scheme. If you can define the first two, you can run the game. The third is only necessary if you want to visualise it.

This folder contains the framework for these files: core methods and imports
are already within. So, every time you want a new game to be simulated:
1. Copy everything in "Base for Any Game" into a new Folder
2. Implement EVERY function in these files
3. ????
4. Profit

### Agents
Minimum dependencies: `Agent_Core`, `game_mechanics`

This contains the concrete implementations (with appropriate Codename) of any Agent subclass.
- Any new Agent should inherit from the Agent class (defined in `Agent_Core`)
- init, update and action MUST be implemented for any concrete Agent
- Note a lot of Agents will just 'wrap' some algorithm, e.g. `Agent_Minimax` is quite succinct

### Algorithms
I wanted a place to store implementation-indepenent, `Agent_Core`/`game_mechanics` dependent python code for any useful algorithm.
- `Node` is a refactoring of the Node class from Part A, except this will work with any `game_mechanics`
- `Minimax` has a refactoring of your code Akira
