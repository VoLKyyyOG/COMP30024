# Algorithms Research

## Covered in COMP30024

### Minimax with alpha-beta pruning
*Idea:* in a two-player game, the game state is measured with a signed integer/real.
- Positive indicates player 1 is winning, negative that player 2 is winning, and zero for neutral.
- Hence, player 1 is 'maximising player' and player 2 is 'minimising'.
- `α` keeps track of the best (already explored) move for a maximisingPlayer.
- `β` keeps track of the best (already explored) move for a minimisingPlayer.
The following algorithm is depth-limited.
1. Construct a directed acyclic graph of game states (nodes) from possible moves to a desired depth.
2. Implement a heuristic (`eval_state_heuristic`) that will assign leaf nodes a score and initialise an `α` and `β` as `-∞` and `+∞` respectively. These are LOCAL to each `minimax()`.
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

**Example**:
- A Minimising grandparent A has Maximising children B and C. B was a left subtree of A and has already been evaluated as 6
- Hence, C will have `β = 6` (so the move that A will make in the worst case is <= 6)
- Assume a child of C's is evaluated as 10
    - C's best possible value (`α`) is now 10 (NB: best relative to C, a maximisingPlayer)
    - This updates C's `α` (due to `α = max(α, value)`)
    - C's best possible move is worse than A's worst-case move (`α` >= `β`)! There is no point further diving into any of C's other children and so C is pruned.

### A*

### UNINFORMED SERACHES: BFS, Uniform Cost Search, DFS, Depth Limited Ssearch, IDA*

## Extracurricular

### Rectangular Symmetry Reduction RSR)

### JPS (improves RSR)

### SSS* (improves A*)

### D* (improves A*)

### Transposition Tables

### Refutation Tables

### Killer Heuristic
*Idea*: 

### Monte Carlo Methods

### Zero-Window Search (adds to Minimax/AB)
