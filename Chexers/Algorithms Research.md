# TO RESEARCH:
- MTD(f) --> apparently outperforms minimax a/b
- Best Node Search --> apparently outperforms MTD(f) and is fairly new
- Use of bloom filters to measure position similarity --> application to killer heuristic?



## A*:
- Best-first search: evaluates nodes with g(n) + h(n) (cost to get here + cost to get to goal). Expand at each step by removing from the 'fringe' (PQ?), update heuristic values, and rinse/repeat until find the goal.
Admissible heuristic --> optimal.
- Need to enforce that you should only add nodes to the 'set to explore' only if their evaluated cost will be less than before

## IDA*:
- Depth-first iterative limited search BUT the limit is not depth but rather a threshold for the f(n). At each iteration, extract minimum cost path found so far. You set threshold to the 'this is what I want optimally, find it' --> if it succeeds, great! If not, you're still going to find the next cheapest fringe progression.
IDA* is beneficial when the problem is memory constrained... A* search keeps a large queue of unexplored nodes...
By contrast... IDA* does not remember any node except the ones on the current path... O(solution) memory space-complexity

## Dijkstra:
- Single-source minimum cost path. Basically A* with h(n) = 0 (no cost heuristic to get to finish considered)

## Floyd-Warshall: PRETTY BAD. O(|V|^3)... |V|x|V| array of all distance combinations. Iterate over each row-col pair and ask if there's shorter. Do this repeatedly (each time = get shortest paths of length total_num_iterations)

#  Minimax + Improvements

## Minimax with alpha-beta pruning
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

# [FS A/B and Aspiration Search info sourced from this fabulous website](https://www.ics.uci.edu/~eppstein/180a/990202b.html)

## Fail-soft alpha beta (extends Minimax)
Fixes one shortcoming of minimax - when a score is uninteresting, no extra information is returned about that score. The reason for this is that the current score is kept in the variable alpha... One of the simplest improvements to alpha-beta is to keep the current score and alpha in separate variables.

```C
// fail-soft alpha-beta search
int alphabeta(int depth, int alpha, int beta) {
    move bestmove;
    int current = -WIN; // maximum score that can be returned by any call
    if (game over or depth <= 0) return winning score or eval();
    for (each possible move m) {
        make move m;
        score = -alphabeta(depth - 1, -beta, -alpha)
        unmake move m;
        if (score >= current) {
            current = score;
            bestmove = m;
            if (score >= alpha) alpha = score;
            if (score >= beta) break;
        }
    }
    return current;
}
```

With this change, one can determine a little more information than before:
- If `x <= alpha`, then we still don't know the true value of the position... but we do know that the true value is at most x.
- Similarly, if `x >= beta`, the true search value is at least x
These slightly tighter upper and lower bounds don't improve the search itself, but they could lead to a greater number of successful hash probes. The use of fail-soft alpha-beta is also essential in the MTD(f) algorithm described below.

## Aspiration Search (introduces idea of a window) (refactoring of A/B)
Normally, when using alpha-beta to choose the best move, one calls `alphabeta(depth, -WIN, WIN)`
where the huge range between -WIN and WIN indicates that we don't know what the true search value will be... instead, it is often helpful to call alpha-beta with an artificially narrow window `prev - WINDOW, prev + WINDOW`. If the result is a score within that window, you've saved time and found the correct search value. But if the search fails, you must widen the window and search again:

```C
// aspiration search
int alpha = previous - WINDOW;
int beta = previous + WINDOW;
for (;;) {
    score = alphabeta(depth, alpha, beta)
    if (score <= alpha) alpha = -WIN; // Must widen window and research, true value outside window
    else if (score >= beta) beta = WIN; // Must widen window and research, true value outside window
    else break; // Window captured actual value
}
```

- The constant WINDOW balances a tradeoff between time savings from a narrower search ... and the time lost from repeating an unsuccessful search.
- Variants of aspiration search include widening the window more gradually in the event of an unsuccessful search, or using a different search window function

## Zero-Window Search (adds to Minimax/AB)
"If a narrower search window leads to faster searches, the idea here is to make the search window as narrow as possible: it always calls alpha-beta with `beta=alpha+1`."
- "The effect of such a "zero-width" search is to compare the true score with alpha: if the search returns a value at most alpha, then the true score is itself at most alpha, and otherwise the true score is greater than alpha."
- Alone, does not hold well for n-player games as the threshold can disguise worser positons as wins *e.g. buying a spoon is of equal value to buying a car if the threshold is just to be able to afford $1.*
- Best used in a complementary fashion when there is reasonable confidence in a parent evaluation, e.g. PVS

## MTD(f) (simplification of alpha-beta)
"The MTD(f) idea is to instead use fail-soft alpha-beta to control the search: each call to fail-soft alpha-beta returns a search value which is closer to the final score, so if we use that search value as the start of the next test, we should eventually converge."
"WARNING: One needs additional code to halt the search if too many iterations have been made without any convergence, as it is susceptible to infinite loops.
```C
// MTD(f)
int test = 0;
for (;;) {
    score = alphabeta(depth, test,test+1);
    if (test == score) break;
    test = score; // Adjusting the window
}
```

## Principal Variation Search (PVS - the 'king' of alpha-beta variants)
"AKA Negascout"
- Alpha-beta search works best if the first recursive search is likely to be the one with the best score... so if we try and make best moves the left-most, we can search the other moves more quickly by using the assumption that they are not likely to be as good. PVS performs an initial search with a normal window, but on subsequent searches uses a zero-width window to test each successive move against the first move. Only if the zero-width search fails does it do a normal search.

```C
// principal variation search (fail-soft version)
int alphabeta(int depth, int alpha, int beta)
{
    move bestmove, current;
    if (game over or depth <= 0) return winning score or eval();
    move m = first move;
    make move m;
    current = -alphabeta(depth - 1, -beta, -alpha) // Evaluate first subtree
    unmake move m;
    for (each remaining move m) {
        make move m;
        score = -alphabeta(depth - 1, -alpha-1, -alpha)
        if (score > alpha && score < beta)
            score = -alphabeta(depth - 1, -beta, -alpha)
        unmake move m;
        if (score >= current) { // Need to update window
            current = score;
            bestmove = m;
            if (score >= alpha) alpha = score;
            if (score >= beta) break;
        }
    }
    return current;
}
```

This shares the advantage with MTD(f) that most nodes in the search tree have zero-width windows, and can use a simpler two-parameter form of alpha-beta. Since there are very few calls with beta > alpha+1, one can do extra work in those calls (such as saving the best move for later use) without worrying much about the extra time it takes.

## Last-branch alpha beta (Zero-window earch applied to Minimax)

## Negamax and variants
This algorithm is a refactoring of the minimax algorithm with same performance and nearly-identical evaluation at each node.
- Rather than assigning nodes the raw heuristic evaluation, each node's score represents the benefit it receives i.e. loss of the other player.
- Each parent attempts to maximise the negated child's scores i.e. minimise the opponent's benefit i.e. maximise the parent's gain!
- Since it's arguably more strenous to understand, **DO NOT USE**

# Random walks and reinforcement learning approaches

## Monte Carlo Tree Search (MCTS): **The planning ahead algorithm**
[Introduction that's easy on the brain](https://medium.com/@quasimik/monte-carlo-tree-search-applied-to-letterpress-34f41c86e238)

[Summary of various methods, HAVE NOT READ YET](http://mcts.ai/pubs/mcts-survey-master.pdf)

MCTS uses randomisation to find the final solution. It is a four-step algorithm:

#### Selection

Choose a node on the tree with highest win evaluation (typically based on stats & how much it's been ignored). A tradeoff exists between exploration and exploitation though, described as the *multi-armed bandit problem*.

**UCB1**:

Uses the below equation to construct confidence intervals for each node (where you are not randomly choosing nodes to expand) and pick the machine with the highest upper bound. Has an growth rate of O(log n) error!
![equation](https://latex.codecogs.com/gif.latex?%5Cfrac%7Bw_i%7D%7Bn_i%7D%20&plus;%20c%5Csqrt%7B%5Cfrac%7Bln%28n_t%29%7D%7Bn_i%7D%7D)

<!-- frac{w_i}{n_i} + c\sqrt{\frac{ln(n_t)}{n_i}} -->

where
- w_i is the number of wins observed at/below this node
- n_i the total of simulations at/below this node
- n_t total simulations
- c a parameter that controls the weighting of exploration (sqrt) over exploitation (wi/ni)

**UCT**: Attempts to improve upon the random tie-breaking of a standard MCTS.
- Enforces that you only descend through nodes that can be treated as a *multi-armed bandit problem*, i.e. there are win/loss statistics available for all its children.
- UCB1 to descend trough the tree you reaching unevaluated node (cannot apply UCB1).


#### Expansion
If that node is non-terminal, create children (what to explore next). Typically only create one, but more advanced forms create all possible children.

#### Simulation
Simulate play of the game for all new nodes until an outcome achieved. Most computationally expensive aspect of the algorithm. Can be done in a "light playout" (a few moves) before making an evaluation or a full playout.

#### Backpropagation
Update the current move sequence with the result, keeping track of which player it benefits (e.g. increment all winning player's w_i, and every node's n_i)

**Eventual decision**: chooses node that incurred most simulations (was, on average, the best place to explore)
- And MCTS is run entirely again from the new starting state

# N-Player Analogs/Approaches

[This paper first introduced MaxN: ](https://www.aaai.org/Papers/AAAI/1986/AAAI86-025.pdf)
- "AI programs tend to analyze partial game trees in order to determine a best move" (due to explosive game tree size)
- "Lookahead procedure" is that which backs up terminal node values to parents (e.g. minimax) and heuristics are what evaluate the terminal nodes

## Paranoid (Reduces N-Player games to Minimax)
This algorithm is an n-player algorithm that assumes all opponents are collectively against the root player. Efficiency drops as n increases (not a concern for us) but does reduce complexity.

*Assumptions*: Opponent behaviour is fixed.

- Identical to a 2-player game, and hence allows for alpha-beta minimax!!!

## Max^n (N-Player Minimax)
[This paper extended MaxN algorithm](https://web.cs.du.edu/~sturtevant/papers/comparison_algorithms.pdf)
This algorithm is an n-player analog of the minimax algorithm. Rather than a singular value representing state evaluation, an n-sized tuple is used, the ith value representing ith players' evaluation, and max_n chooses the child node of a player with tuple that maximises the choice player's score.

*Assumptions*: Opponent behaviour is fixed.

**Pruning in max_n with shallow pruning does not yield asymptotic gains theoretically, and deep pruning is unreliable** - this is suggestedly because it is based on only 2 of n players for max_n, rather than the effectively exhaustive comparison of a minimax pruning mechanism.

**Tie-breaking rules impact a tree valuation** - however taking a paranoid approach and assuming opponents will attempt to minimise EITHER a certain player OR us specifically will allow us to prune ties that could allow opponents to do just that.

**Overall**: Max_n tends to yield better results than paranoid where pruning is likelier to be possible, and worse when brute-force is the common/likeliest approach.

[Sturtevant's remedy](https://www.cs.du.edu/~sturtevant/papers/spec_prune.pdf)
## Speculative/last-branch pruning (improves Max_n)
**WARNING**: This only gets to decisions faster than without it, but evaluations are equivalent i.e. *Paranoid still wins.*

*Requires*: lower bound on individual scores and maximum on sum of all scores

*Idea/lemma*: If in a max_n tree, sum(lower_bounds) for a consecutive player sequence meets/exceeds max_sum, the max_n value of any child of the most recent player in the sequence cannot best the game tree.

**Last-branch pruning**: Where the lemma conditions are met, pruning children of the most recent player will be correct IF
1. The intermediate player(s) in the sequence are searching their last branch.
- i.e. Player 1 can only prune a Player 3's decision if Player 2 is on their last-branch. *WHY? Because under the lemma conditions, it would be impossible for the most recent player 3 to choose a better move that BOTH the previous player 2, and the current player 1, could benefit from (as the bounds limit growth to one player at the other's expense)*
2. The best max_n value from the intermediate player(s)' previously searched children cannot trump Player 1's current bound.

**Speculative pruning**: Last-branch pruning that doesn't wait until last branch for intermediate branches, but is willing to re-search if necessary (i.e. where Player 2 and Player 1 could mutually benefit from another Player 2 branch that wasn't explored at the time of pruning).
*Note: sub-optimal ordering forces re-search because it forces Player 1 to change its preference to the current sub-branch, rather than a prior. This upsets the bounds that uphold the lemma for pruning to work, and hence, fields must be re-evaluated in the subbranch we pruned.*

Sturtevant pseudocode (adapted) for speculative pruning
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

## Directed Offensive (DO)
*Idea*: Root player chooses a target to attack and aims to minimise their score, but assumes opponents are greedy.
- Allows for pruning when a (sufficiently) worst-case evaluation is returned
- Does NOT allow shallow pruning

## MP-Mix (Dynamic strategy in N-Player games)
[Created by Inon Zuckerman and Ariel Felner](http://www.ise.bgu.ac.il/faculty/felner/papers/2011/Journal_mixed.pdf)  

*Idea*: If strongly winning, play defensively (Paranoid). If another player is strongly winning, play offensive towards them to prevent your likely loss (Directed Offensive). Otherwise, play greedy (MaxN).
*Implement as a vector of weights w*: maximisingPlayer prefers a to b if dotP(w,a) > dotP(w,b).
- Paranoid/DO: `w[winningPlayer] = (2*(winningPlayer == me) - 1), all others 0` (works for both the winner and non-winner players)
      - *Play DO when*: `not_first && diff(1st, 2nd) > offensiveThreshold`
      - *Play Paranoid when*: `am_first && diff(1st, 2nd) > defensiveThreshold`
- MaxN: `w[you] = 1, all others 0`
      - Play MaxN if not playing DO/Paranoid
*Best applications*: Where **OI** (empirical/theoretical % of all states in a game that allow for moves that impede an opponent) is high. However, all this relies on the game and evaluation functions used.

Pseudocode
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

# Tabular techniques/search memoization

## Refutation Tables
'Abandoned', modern programs use transposition tables and killer heuristic typically.

## Butterfly Board

## Killer Heuristic
*Idea*: A move that was strong in some subtree X *could* also be strong in another location Y where the game states are similar enough. Typcically a killer move is one that doesn't explicitly capture, but causes cutoffs/trimming down the tree.
- Requires a certain measure of similarity of states, and flexibility to allow for higher priority children
