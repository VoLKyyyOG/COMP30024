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

### To Dos:
- Play the game (print on cardboard and see how that goes)
- Find positions that are weighted more crucially compared to others

### MP-Mix Algorithm:
[Created by Inon Zuckerman and Ariel Felner](http://www.ise.bgu.ac.il/faculty/felner/papers/2011/Journal_mixed.pdf)  
[Here is the MaxN algorithm](https://web.cs.du.edu/~sturtevant/papers/comparison_algorithms.pdf)  
All these approaches (MaxN, Paranoid and Offensive) are fixed.  We introduce the MaxN-Paranoid mixture (MP-Mix) algorithm, a multi-player  adversarial search algorithm which switches search strategies according to the game situation. MP-Mix is a meta-decision algorithm that outputs, according to the players’ relative strengths, whether the player should conduct a game-tree search according to the MaxN principle, the Paranoid principle, or the newly presented Directed Offensive principle. Thus, a player using the MP-Mix algorithm will be able to change his search strategy dynamically as the game develops.

**Offensive Principle:**
Before discussing the MP-Mix algorithm we first introducea  new  propagation  strategy  called  the  Directed  Offensive strategy (denoted *offensive*) which complements the Paranoid strategy in an offensive manner. In this new strategy the root player first chooses a target opponent he wishes to attack. He then  explicitly  selects  the  path  which  results  in  the  lowest evaluation  score  for  the  target  opponent.  Therefore,  while traversing  the  search  tree  the  root  player  assumes  that  the opponents  are  trying  to  maximize  their  own  utility  (just  as they  do  in  the  MaxN  algorithm),  but  in  his  own  tree  level she selects the lowest value for the target opponent. This will prepare the root player for the worst-case where the opponents are not yet involved in stopping the target player themselves. In  this  case,  player  2  will  select  the best nodes with respect to his own evaluation (ties are broken to  the  left  node). As   stated   above,   if   coalitions   between   players   can   beformed  (either  explicitly  via  communication  or  implicitly  by mutual understanding of the situation), perhaps several of the opponents  will  decide  to  join  forces  in  order  to  “attack”  and counter  the  leading  player,  as  they  realize  that  it  will  give them a future opportunity to win. When this happens, the root player can run the same offensive algorithm against the leader but under the assumption that there exists a coalition against the  leader  which  will  select  the  worst  option  for  the  leader and not the best for himself.


**ELI5:**
If the current leader is the **root player**, the agent uses the **Paranoid Strategy** (*the agent will assume all other players want to hurt it*). However, if the current leader is **NOT** the **root player**, the agent will then use the **Offensive Strategy** (*the agent will attempt to worsen the situation of the leading player*).

**Pseudocode:**
```
for each i ∈ Players do:
    H[i] = evaluate(i);
    endsort(H);         // decreasing order sorting
    leadingEdge = H[1] − H[2];          // the two leaders
    leader = identity of player with highest score;
    if (leader = root player) then:    
        if (leadingEdge ≥ Td) then:
            Paranoid(...);
            end
    else:
        if (leadingEdge ≥ To) then:
            Offensive(...);
        end
    end
MaxN(...);
```
MP-Mix(Td,To)
