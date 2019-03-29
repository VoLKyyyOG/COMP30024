# Part A - Report.pdf

## Authors: Callum H, Akira W
## Team: _blank_

MUST BE TWO PAGES LONG max

# Focus questions

#### How have you formulated the game as a search problem?
(You could discuss how you view the problem in terms of states, actions, goal tests, and path costs, for example.)

#### What search algorithm does your program use to solve this problem, and why did you choose this algorithm?
(You could comment on the algorithm’s efficiency, completeness, and optimality. You could explain any
heuristics you may have developed to inform your search, including commenting on their admissibility.)

#### What features of the problem and your program’s input impact your program’s time and space requirements?
(You might discuss the branching factor and depth of your search tree, and explain any other features of the
input which affect the time and space complexity of your algorithm.)

## Problem Formulation (answers Q1)
- Fully Observable, Deterministic, Sequential, Static, and Discrete
- States: the exact number and positions of each player piece, and each block. 
- Actions: Move, Jump, and Exit (pass if there is no possible move)
- Goal tests: 
- Path costs: The minimum number of actions required to reach goal

## Algorithmic Approach

### Heuristic

1. Dijkstra's
    - Pre-calculates cost from each position to the possible unblocked goal(s)
    - Essentially a mapping function
    - Expensive-ish precomputation but makes up for boards with a several action move sequence 
2. A "Jump" Manhattan
    - Assumes a "Jumping" world scenario
    - Admissible
    - `ceil(3 - current row/2) + 1`

#### Explain and justify

### Search algorithm

1. IDA*
    - Your classic and lovable IDA* because A* was too pleb
    - Iterative Deepening A*
    - Rather than generating nodes, we expand them (saves plenty of unnecessary nodes)
    - Space Efficient (doesn't keep a set of nodes that we intend to visit). This is important due to the number of nodes we may possibly generate for a several action move sequence - running that on Dimefox may be suicidal
    - Doesn't use dynamic programming and therefore may explore the same nodes several times

2. Transposition Table (TT)
    - Callum's blood and sweat thus named (T^T)
    - Since we have a fully observable state, we are able to use the TT to use memoization
    - Hash table which also uses a hashing function `Z_Hash` to keep track of visited states so we don't explore them
    - Prevents not only repeating moves, but symmetric states ($n$ moves later if we reach the same state)


#### Explain and Justify

## Effectiveness of Approach

### Asymptotic Time-Space Complexity Analysis
- Many nodes
- Also we like to perform mass genocides on the nodes
- Roughly 60% nodes or pruned using the TT
- (use valgrind for space or just the number of bytes generated for nodes?)
- Time is pretty fast now even for the hardest of problems 

### Branching (does it get dense? Is it wasting time on expansions?)
What does the problem contribute to this issue?
Does the input or its features impact this?
What features of the problem allowed us to reduce branching?

### Depth (does it explore beyond optimal depth?)
What does the problem contribute to this issue?
Does the input or its features impact this?
What features of the problem allowed us to reduce branching?

IDA* IS OPTIMAL YEEEE
