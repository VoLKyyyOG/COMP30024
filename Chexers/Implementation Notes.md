# Implementation Notes

## My updates 20/03/2019 (a copy of the github merge description)
It's Wednesday, yay I can finally code.
Few major changes:
1. One of the goals was wrong, so I fixed that.
2. Made minor naming alterations to Node and moves.py to improve readibility (e.g. replaced move with action whenever action was meant, and not the actual 'move to an adjacent' move the game describes.)

3. Partly implemented IDA* to work with current classes, including creating a subclass IDA_Node that inherits the Node properties but also pre-initialises travel_cost and exit_cost for you. It doesn't have to be used, but it makes it very clear what a node is intended to be used for.

4. Coded the admissible 'max-displacement' heuristic we were discussing using cubic coordinate form (Vector.get_cubic())

5. Moved hash.py into classes.py

6. Slightly modified flags in Z_hash for better heuristic implementation, nothing major.

7. Added INF

## Plan of Attack for Part A:
- 1. Use IDA* to explore. Requires admissibility!
    - g(n) is cost to get here, = 2*moves + jumps.
    - h(n) ideally derived from children, and should *try* to consider jumping possibilities.
        - IDEA: Take distance_to_exit / 2 (this way, jumping cannot exceed the heuristic e.g. ADMISSIBLE)
- 2. Use a mega transpositon table to capture 'across the branch repetition' (i.e. RSR) and 'down the branch' (li.e. kill inf loops)
    - WHY: prop. leaf nodes of all generated nodes ~ 95% (so making tons of copies is BAD IDEA)
    - TT: a defaultdict(int). Keys of the form hash(state): instance.
    - If you want to get 'down the branch' history: iterate through hash(instance.state) until you hit null (starting position)
    - If you want to check 'across the branch': check if hash(state) in TT.keys!

## Callum's Notes:
- *Consider* getting VS Code
- Refactor Node code for optimal access (prioritise abstraction and readability)
- OrderedDict allows equality!
- `__iadd__` for in-place addition (+= stuff)
- Sequential players determinable by x+1 % 3... ref global dict for string form
- Explore mapping \**kwargs to attributes --> `setattr(self, key, value)`
- Classes, lists, dicts are MUTABLE -> x1 = class and x2 = x1 copies the reference. Edits to x1 can be made that impact x2, however directly re-assigning either will break the link (new object wins)
- ADVANCED GOAL: Attempt 'colour rotational' symmetry reduction in N-player case (whose turn it is is important)
- ADVANCED GOAL: Sound TT implementation + solving outlined issues

# SOME IDEAS FOR ALGORITHMS/HEURISTICS (NOT ACTUAL RESEARCH, JUST BRAINSTORMS)

## Heuristic for Part A BRAINSTORM:
- Admissible: cost evaluation <= actual solution cost (does NOT over-estimate)
- Consistent: monotonic. Not very likely...
Ideas:
- "Row displacement": # perp. rows away from disappearing (e.g. pieces on
- Should be f(n) = g(n) + h(n). G(n) is "cost to get here" (using move = 2, jump = 1 is simple)
- h(n) or "cost to exit" is reliant on the children evaluation.

## For Paranoid/Directed Offensive + AB :
- data = (root, a, b)
- (same fxn, outcome dpt on root vs curr_player)
- MUST use tuples/immutables for arguments to NOT be an alias (local to each call)

## RSR for semi-static env (dynamic only if piece identity changes)
- Note: this is NOT TT - TT is duplicates 'down the branch', RSR is 'across the branch'
- Idea: "Best" with ID search algorithms?
- Q: RSR benefits from moved_piece (attach to parent) --> in data OR as an attribute?
- Method A: Explore all child paths where root piece is moved
- 1. Detect path networks of same piece (just ignore other children that aren't)
- 2. Perform RSR on THOSE PATHS, and only on children with SAME piece
- 3. Same boards are same = if you can RSR, do it! Don't worry a/b alternate piece choices
