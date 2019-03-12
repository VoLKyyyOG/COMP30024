# Algorithms Research

## Covered in COMP30024

![equation](https://latex.codecogs.com/gif.latex?frac{w_i}{n_i}&space;&plus;&space;c\sqrt{\frac{ln(n_t)}{n_i}})

![equation](https://latex.codecogs.com/gif.latex?frac%7Bw_i%7D%7Bn_i%7D%20&plus;%20c%5Csqrt%7B%5Cfrac%7Bln%28n_t%29%7D%7Bn_i%7D%7D)

### Minimax with alpha-beta pruning
*Idea:* in a two-player game, the game state is measured with a signed integer/real.
- Positive indicates player 1 is winning, negative that player 2 is winning, and zero for neutral.
- Hence, player 1 is 'maximising player' and player 2 is 'minimising'.
- `α` keeps track of the best (already explored) move for a maximisingPlayer.
- `β` keeps track of the best (already explored) move for a minimisingPlayer.

*Assumptions*: Has access to a reasonable heuristic (**THIS IS THE MAIN PROBLEM**)

The following algorithm is depth-limited.
1. Construct a directed acyclic graph of game states (nodes) from possible moves to a desired depth.
2. Implement a heuristic (`eval_state_heuristic`) that will assign leaf nodes a score and initialise an `α` and `β` as `-∞` and `+∞` respectively. These are LOCAL to each `minimax()`.
2. Perform the minimax DFS algorithm:

[Pseudocode (adapted)](https://en.wikipedia.org/wiki/Minimax#Minimax_algorithm_with_alternate_moves)
```python
def minimax(node, depth, α, β, maximizingPlayer):
    if (depth == 0) or (node is leaf node):
        return (evaluate_state(node))
    if maximizingPlayer:
        value = −∞
        for each child of node:
            value = max(value, minimax(child, depth − 1, α, β, False))
            ######### ONLY FOR ALPHA-BETA
            α = max(α, value) # Only updates if this child just beat previous
            if α >= β: break
            #########
        return value
    else: # minimizing player
        value = +∞
        for each child of node:
            value = min(value, minimax(child, depth − 1, True))
            ######### ONLY FOF ALPHA-BETA
            β = min(β, value) # Only updates if this child just beat previous
            if α >= β: break
            #########
        return value
```

4. Call `minimax(origin, depth, α, β, True)` to run.

**Example**:
- A Minimising grandparent A has Maximising children B and C. B was a left subtree of A and has already been evaluated as 6
- Hence, C will have `β = 6` (so the move that A will make in the worst case is <= 6)
- Assume a child of C's is evaluated as 10
    - C's best possible value (`α`) is now 10 (NB: best relative to C, a maximisingPlayer)
    - This updates C's `α` (due to `α = max(α, value)`)
    - C's best possible move is worse than A's worst-case move (`α` >= `β`)! There is no point further diving into any of C's other children and so C is pruned.

### A*

### UNINFORMED SEARCHES: BFS, Uniform Cost Search, DFS, Depth Limited Ssearch, IDA*

## Extracurricular

### Monte Carlo Tree Search (MCTS): **The planning ahead algorithm**
[Introduction that's easy on the brain](https://medium.com/@quasimik/monte-carlo-tree-search-applied-to-letterpress-34f41c86e238)
[Summary of various methods, HAVE NOT READ YET](http://mcts.ai/pubs/mcts-survey-master.pdf)

MCTS uses randomisation to find the final solution. It is a four-step algorithm:
#### Selection

Choose a node on the tree with highest win evaluation (typically based on stats & how much it's been ignored). A tradeoff exists between exploration and exploitation though, described as the *multi-armed bandit problem*.

**UCB1**:
https://latex.codecogs.com/gif.latex?%5Cfrac%7Bw_i%7D%7Bn_i%7D%20&plus;%20c%5Csqrt%7B%5Cfrac%7Bln%28n_t%29%7D%7Bn_i%7D%7D

where
- w_i is the number of wins observed at/below this node
- n_i the total of simulations at/below this node
- n_t total simulations
- c a parameter that controls the weighting of exploration (sqrt) over exploitation (wi/ni)

<!-- frac{w_i}{n_i} + c\sqrt{\frac{ln(n_t)}{n_i}} -->

#### Expansion
If that node is non-terminal, create children (what to explore next). Typically only create one, but more advanced forms create all possible children.

#### Simulation
Simulate play of the game for all new nodes until an outcome achieved. Most computationally expensive aspect of the algorithm.

#### Backpropagation
Update the current move sequence with the result, keeping track of which player it benefits (e.g. increment all winning player's w_i, and every node's n_i)

**Eventual decision**: chooses node that incurred most simulations (was, on average, the best place to explore)
- And MCTS is run entirely again from the new starting state

### UCT

### Paranoid (complements Minimax)
This algorithm is an n-player algorithm that assumes all opponents are collectively against the root player. Efficiency drops as n increases (not a concern for us) but does reduce complexity.

*Assumptions*: Opponent behaviour is fixed.

- Identical to a 2-player game, and hence allows for alpha-beta minimax!!!

### Zero-Window Search (adds to Minimax/AB)
This 2-player zero-sum algorithm asserts all leaves must evaluate to a win or loss by use of a threshold v.
- Does not hold well for n-player games as the threshold can disguise worser positons as wins *e.g. buying a spoon is of equal value to buying a car if the threshold is just to be able to afford $1.*

### Max^n (extends Minimax)
This algorithm is an n-player analog of the minimax algorithm. Rather than a singular value representing state evaluation, an n-sized tuple is used, the ith value representing ith players' evaluation, and max_n chooses the child node of a player with tuple that maximises the choice player's score.

*Assumptions*: Opponent behaviour is fixed.

**Pruning in max_n with shallow pruning does not yield asymptotic gains theoretically, and deep pruning is unreliable** - this is suggestedly because it is based on only 2 of n players for max_n, rather than the effectively exhaustive comparison of a minimax pruning mechanism.

**Tie-breaking rules impact a tree valuation** - however taking a paranoid approach and assuming opponents will attempt to minimise EITHER a certain player OR us specifically will allow us to prune ties that could allow opponents to do just that.

**Overall**: Max_n tends to yield better results than paranoid where pruning is likelier to be possible, and worse when brute-force is the common/likeliest approach.

[Sturtevant's remedy](https://www.cs.du.edu/~sturtevant/papers/spec_prune.pdf)
### Speculative/last-branch pruning (improves Max_n)
**WARNING**: This only gets to decisions faster than without it, but evaluations are equivalent i.e. *Paranoid still wins.*

*Requires*: lower bound on individual scores and maximum on sum of all scores

*Idea/lemma*: If in a max_n tree, sum(lower_bounds) for a consecutive player sequence meets/exceeds max_sum, the max_n value of any child of the most recent player in the sequence cannot best the game tree.

**Last-branch pruning**: Where the lemma conditions are met, pruning children of the most recent player will be correct IF
1. The intermediate player(s) in the sequence are searching their last branch.
- i.e. Player 1 can only prune a Player 3's decision if Player 2 is on their last-branch. *WHY? Because under the lemma conditions, it would be impossible for the most recent player 3 to choose a better move that BOTH the previous player 2, and the current player 1, could benefit from (as the bounds limit growth to one player at the other's expense)*
2. The best max_n value from the intermediate player(s)' previously searched children cannot trump Player 1's current bound.

**Speculative pruning**: Last-branch pruning that doesn't wait until last branch for intermediate branches, but is willing to re-search if necessary (i.e. where Player 2 and Player 1 could mutually benefit from another Player 2 branch that wasn't explored at the time of pruning).
*Note: sub-optimal ordering forces re-search because it forces Player 1 to change its preference to the current sub-branch, rather than a prior. This upsets the bounds that uphold the lemma for pruning to work, and hence, fields must be re-evaluated in the subbranch we pruned.*

Sturtevant pseudocode (adapted)
```python
def specmax_n(Node, ParentScore, GrandparentScore)
    # note: result[currentPlayer] = "guaranteed score for currentPlayer from that subtree"
    # "To prune Node A" is to stop checking it's children, and to evaluate it as
    # NIL because neither it, nor its parent, will be (speculatively) chosen by
    # the grandparent as it's history is far preferred.

    best = NIL, specPrunedQ = NIL
    if terminal(node): return evaluate_state(node)

    for each child of Node:
        if (ParentScore >= best[previousPlayer]):
            # The parent will still prefer its previously explored branches to
            # the currently explored children: still a chance to kill this Node
            result = specmax_n(next child(Node), best[currentPlayer], ParentScore)
        else:
            # The parent finds one of this Node's children preferable to its history
            # So GUARANTEE that you will NOT prune any other children: these
            # will be further explored as now the Parent is interested.
            result = specmax_n(next child(Node), best[currentPlayer], 0)

        # If no best to compare to, this is first child of Node - it is best!
        if (best == NIL): best = result
        # The best satisfies the lemma - the current should be pruned - kill it!
        else if (result == NIL): add Child to specPrunedQ
        # Should compare best to result, and pick that which maximises currentPlayer!
        else if (best[currentPlayer] < result[currentPlayer]):
            best = result
            # If this new result will be preferred by the parent, we need to
            # re-search the NIL node (a depth below this node) as the bounds of parents will be
            # disturbed upon the Parent rejecting its prior observed best.
            if (ParentScore > best[previousPlayer]):
                re-add specPrunedQ to child list

        # Below is only true if the best Node meets maxsum threshold.
        # This means that any new Node's children, if preferred, would reduce parent/Gparent scores.
        # But no perfect logician would choose any path that would do this.
        # Hence, skip the rest of this Node's children --> i.e. this Node is pruned!
        if (GrandparentScore + ParentScore + best[currentPlayer] >= maxsum): return NIL
    # This node has determined it should not be pruned
    return best
```

**Discrete Cutoff Evaluations**: where the `evaluate_state()` guarantees a minimum difference in evaluation of d for any player at any instance. We can prune where sum(scores) >= maxsum - d(n-2)

### Directed Offensive (DO)
*Idea*: Root player chooses a target to attack and aims to minimise their score, but assumes opponents are greedy.
- Allows for pruning when a (sufficiently) worst-case evaluation is returned
- Does NOT allow shallow pruning

### MP-Mix (strategically dynamic improvement on Paranoid, MaxN)
*Idea*: If strongly winning, play defensively (Paranoid). If another player is strongly winning, play offensive towards them to prevent your likely loss (Directed Offensive). Otherwise, play greedy (MaxN).
*Implement as a vector of weights w*: maximisingPlayer prefers a to b if dotP(w,a) > dotP(w,b).
- Paranoid/DO: `w[winningPlayer] = (2*(winningPlayer == me) - 1), all others 0` (works for both the winner and non-winner players)
      - *Play DO when*: `not_first && diff(1st, 2nd) > offensiveThreshold`
      - *Play Paranoid when*: `am_first && diff(1st, 2nd) > defensiveThreshold`
- MaxN: `w[you] = 1, all others 0`
      - Play MaxN if not playing DO/Paranoid
*Best applications*: Where **OI** (empirical/theoretical % of all states in a game that allow for moves that impede an opponent) is high. However, all this relies on the game and evaluation functions used.

[Pseudocode Source](http://www.ise.bgu.ac.il/faculty/felner/papers/2011/Journal_mixed.pdf)
```python
def MP_mix(defensiveThreshold, offensiveThreshold):
    for each i ∈ Players:
        H[i] = evaluate(i)
    sort(H)                           # decreasing order sorting
    leadingEdge = H[1] − H[2]         # the two leaders
    leader = identity of player with highest score;
    if (leader = root player):    
        if (leadingEdge ≥ defensiveThreshold):
            return Paranoid(...)
    else:
        if (leadingEdge ≥ offensiveThreshold):
            return Offensive(...)
    return MaxN(...)
```
**OI**: Measures impact of a decision on other players' performance. Typically, agents whose strategy = function(OI) perform better --> hence, constant OI tends to imply a constant strategy agent will work well.

### Rectangular Symmetry Reduction (RSR)

### JPS (improves RSR)

### SSS* (improves A*)

### D* (improves A*)

### Transposition Tables

### Refutation Tables

### Killer Heuristic
*Idea*: A move that was strong in some subtree X *could* also be strong in another location Y where the game states are similar enough.
