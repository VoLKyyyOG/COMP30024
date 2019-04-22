# Guide to Part B Folders
## Akira - To Date
- `Runner` agent uses Paranoid with `speed_demon` heuristics.
- A couple functions were cleaned / fixed (notably `all_dead` has been fixed to trigger for when TWO players are dead, not one - oops my bad)
- Original referee was added back in, the modified one is now called `referee_mod` and can be called the same as usual
- Possible actions now has a `paranoid_play` flag, will most likely require a `offensive_play` flag which calls `paris` if `True`.
  - This is broken for now (for some reason it returns `None` even though it shouldnt...)
- `retrograde_dijkstra` and `dijkstra_board` was changed to work for Part B. I've assumed `occupied` to now be any piece.
  - Problem is that our assumption from Part A where we have at most 4 pieces is incorrect (`retrograde_dijkstra` will sum all pieces we have)
  - Hypothetically just need to add the closest (4 - number_of_exits) pieces into retrograde_dijkstra.
  - Maybe `speed_demon` also suffers the same issue. After several runs with `Runner` against `Greedy` or `Random`, I've found that `speed_demon` will almost always end in a repeated state (4 times causing a draw) since it tries to make every piece closer to the goal. The fix should be the same for `retrograde_dijkstra`
- Added a `master` heuristic which acts as the evaluation function for `negaparanoid` and most likely `mp_mix`.
  - Essentially has a list of costs per player, for each heuristic we decide to use.
  - Returns a "weighted" sum of the heuristic costs
- `max_n` was implemented and works. 3-ply is very fast, but 4-ply is insanely slow but yields great results. 
  - WIll look into lazy evaluation (but that's related to the heuristic), immediate pruning (still need to find what the `max` utility value will be, and can only be done after heuristics are finalised), shallow pruning (need to do more research on this...)
- `mp-mix` Agent now uses a mix of `negaparanoid` and `max_n` and switches based on the logic we've implemented. Any `DirectedOffence` call has been redirected to just use `max_n`

## Notes to self (Callum)
TODO:
1. Implement N-Player MC
2. Streamline Algorithm Storage to work with states, and then with nodes
  - Eventual idea: want some data to remain, store this as a node bundle

Other:
- Be careful about negamax negation as you might accidentally negate your own valuation
- Too complex a heuristic = can lose sight of reality. Quiescence/raw search power must always triumph. Simple > complex
- Beware the relationships b/t heuristics: you don't want a case where (benefit from exiting) < (loss due to perceived desperation) (note that could never happen as exiting preserves desperation but still)
- Choose transformations of 'raw' heuristics wisely e.g. does a +1 in desperation outweight a +0.2 in paris?
- adjust achilles_h, paris_h, desperation:
    - For a 0-1 uniform distribution (0 bad, 1 awesome), `achilles_h[i] = (potential_max_achilles - actual) / (potential_max_achilles - potential_min_achilles)` where potentials are unique to each player and to each state
    - For a 0-1 uniform distribution (0 bad, 1 awesome), `paris_h[i] = (actual - potential_min_paris) / (potential_max_paris - potential_min_paris)` where potentials are unique to each player and to each state
    - desperation[i] = actual * abs(actual)--> this way slight lead/loss is +-1, big lead/loss is += 4, etc.
        - This and transformations of other allow a simple 'too awesome'/'too terrible' pruning schema where absolutely horrible positions are avoided
- all heuristics can be informative in different ways:
    - Achilles (as described above) just informs on your own proportional strength. However a high `achilles_leader_edge` means your opponents are very vulnerable and they won't attack you in the short term. Similarly a low `achilles_rival_edge` means the 'weaker' player may be in a position to attack the mid-range, which benefits the leader. This assumes they play a similar strategy though.
    - Similarly a high `paris` could mean you are in an unstable, complex position and hence should go deeper on quiescence to 'get the right moves'.
- paris is a short-term evaluation to detect complex playouts - if it is zero, your quiscence doesn't have to be as deep

## Motivations
Since we wanted to test many different games before we attack Chexers,
and with many different algorithms, we wanted a code structure that:
1. Allowed you to code algorithmic approaches independent to any game (coding to an interface)
2. Allowed easy one-hit coding for any game that coheres with the above (implementing the interface)
3. Was consistent

## How to Run a Game
To run any game, the following files/structure is necessary:

```pseudocode
./mechanics.py        # fully defines a ton of functions
./referee/            # Includes CUSTOM referee files that work with any game
./player/             # Folder for any number of players to use for game
    __init__.py   # Make it a package. Blank file
    generic_1/        # Folder
        __init__.py   # See Player_example for code
        player.py     # See Player_example - implements \_\_init\_\_, update and action
    generic_2/
    etc...
```

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
