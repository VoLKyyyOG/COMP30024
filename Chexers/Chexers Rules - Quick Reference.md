# General rules

## Game design
- 3 players (RGB) on a hexagonal board of 37 hexes (4-sided hexagon)
- Players start with 4 pieces
- Turn pattern: R --> G --> B --> R...

## Actions available per player

### Move Action
A piece is moved from current hex to an adjacent, empty hex.

### Jump Action
A piece can move straight over one occupied, adjacent hex to a directly adjacent empty hex.
Any opponent piece jumped over is **converted** to become the moving players'.

### Exit Action
A piece located in an appropriate exit hex leaves the board and scores. You cannot *jump* and exit.

### Pass
Only if no other action available. No action is taken.

## Endgame condition
The game ends when one player has taken 4 exiting actions; they are declared winner and other players have incurred a loss.
The game is declared a *draw* if:
1. A board configuration occurs for the fourth time in the game, not necessarily in succession.
2. Each player has had 256 turns (includes passes) with no winner declared.

**Board configuration**: Uniquely identifies a board state, where the same pieces occupy same hexes on the same players' turn. *Permutations of each players' pieces are ignored.*