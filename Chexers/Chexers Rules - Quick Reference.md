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

### States:
-   Coordinate location of the **pieces** on a board consisting of 37 *hexes*
-  Would it be better to use `1 - 37` to denote positions or an `i,j` representation in a matrix?

### Actions:
- Move player piece left, right, up, down
- Jump over a piece GIVEN the directly adjacent hex is empty (Should be a high positive rating)
- Exit the board (Set to INTMAX or +inf

### Goal State:
- 4 pieces completing an **exit action**
- All other pieces have been converted to yours

### Path Cost:
- 3 per move (n-Players I believe???)