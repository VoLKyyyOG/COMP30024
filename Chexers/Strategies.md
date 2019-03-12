Chexers Strategies
====
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

### Evaluation:
- Completeness (play to win or to gain max benefits)
- Time Complexity (number of generated nodes)
- Space Complexity (max number of nodes in memory)
- Optimality (Does it always find the least-cost solution?)

### Things to take into consideration:
- Let (p1, p2, p3) represent the zero-sum for player 1, player 2 and player 3:
    - For player 1, does a (5, 2 , 7) weigh better than a (5, 4, 4)?
    - If a player is out, how do we put it into consideration (-INTMAX or -inf)

### Opening Stage:
1. Play random / safe moves until another piece is capturable
2. Move so that they are in groups that cannot be captured?
3. *Look into finding moves that are more likely to win (such as corner tile heuristics for n-puzzles, centre column connect 4, 4 move checkmate in chess, etc)*

### Mid Stage:
1. Blocking **exit actions** for opponents
2. Attempt to convert all opponent pieces
3. Do a runner to the edge and attempt to exit the board

### End Game:
- *What if an exit move comprimises your win (you have 2 pieces where one is an exit move whilst the other could be converted, and you have only had 2 exits)*
- Sacrificing pieces that are irrelevant to an exit move (decoy pieces?)

### To Dos:
- Play the game (print on carboard and see how that goes)
- Find positions that are weighted more crucially compared to others

