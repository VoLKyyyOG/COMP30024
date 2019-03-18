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
    - **C: I think we should implement the game to handle variable board size (e.g. side 3) to allow greater computational power when exploring algorithmic choices.**

### Evaluation:
- Completeness (play to win or to gain max benefits)
- Time Complexity (number of generated nodes)
- Space Complexity (max number of nodes in memory)
- Optimality (Does it always find the least-cost solution?)

### Things to take into consideration:
- Let (p1, p2, p3) represent the zero-sum for player 1, player 2 and player 3:
    - For player 1, does a (5, 2 , 7) weigh better than a (5, 4, 4)?
    - If a player is out, how do we put it into consideration (-INTMAX or -inf)
- *C: Whenever a heuristic/evaluation generates paths, can we store it for future reference to prevent computational waste?*

### Opening Stage:
1. Play random / safe moves until another piece is capturable
2. Move so that they are in groups that cannot be captured?
3. *Look into finding moves that are more likely to win (such as corner tile heuristics for n-puzzles, centre column connect 4, 4 move checkmate in chess, etc)*
**C: I think it's safe to assume that attaining center presence > staying on the edges, on the basis that centre = more maneouvrability and will threaten other players**

### Mid Stage:
1. Blocking **exit actions** for opponents
2. Attempt to convert all opponent pieces
3. Do a runner to the edge and attempt to exit the board

### End Game:
- *What if an exit move compromises your win (you have 2 pieces where one is an exit move whilst the other could be converted, and you have only had 2 exits)*
- Sacrificing pieces that are irrelevant to an exit move (decoy pieces?)
     - **Could be resolved if evaluation heuristic can simulate a few moves ahead, ascertains a valuable move is possible**
