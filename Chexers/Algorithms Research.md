# Algorithms Research

## Covered in COMP30024

### Minimax with alpha-beta pruning
*Idea:* in a two-player game, the game state is measured with a signed integer/real.
- Positive indicates player 1 is winning, negative that player 2 is winning, and zero for neutral.
- Hence, player 1 is 'maximising player' and player 2 is 'minimising'.
The following algorithm is depth-limited.
1. Construct a directed acyclic graph of game states (nodes) from possible moves to a desired depth.
2. Implement a heuristic (`eval_state_heuristic`) that will assign leaf nodes a score and initialise an `α` and `β` as `-∞` and `+∞` respectively. These are NOT local to `minimax()`.
2. Perform the minimax DFS algorithm:
**Source**: https://en.wikipedia.org/wiki/Minimax#Minimax_algorithm_with_alternate_moves
```python
def minimax(node, depth, α, β, maximizingPlayer):
    if (depth == 0) or (node is leaf node):
        return (eval_state_heuristic(node))
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

*Intuition*:
- `α` keeps track of the least positive move that a maximisingPlayer could choose.
- `β` tracks the least negative move that a minimisingPlayer could choose.
- Using minimax, a maximisingPlayer updates `α` as the algorithm explores the nodes below it. Of course, the leftmost subtree has to be evaluated before any optimisations/pruning can be done: let's say this assigns `α` the value `α_left` (the best move the player can make from the leftmost subtree)
- Eventually, the algorithm descends into other subtrees of this player and realises
- A `maximisingPlayer`

`αβ`


### A*

## Extracurricular

### Rectangular Symmetry Reduction RSR)

### JPS (improves RSR)

### SSS* (improves A*)

### D* (improves A*)

### Transposition Tables

### Refutation Tables

### Killer Heuristic

### Monte Carlo Methods

### Zero-Window Search (adds to Minimax/AB)
