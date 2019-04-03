# Part A - report.pdf

## Authors: Callum Holmes (899251), Akira Wang (913391)
## Team: _blank_

MUST BE 1-2 pages STRICTLY

### FOCUS QUESTIONS ARE ITALICISED

#### *How have you formulated the game as a search problem?
(You could discuss how you view the problem in terms of states, actions, goal tests, and path costs, for example.)*

## Problem Formulation (answers Q1)

The problem of navigating pieces across a Chexers board to successful exit is:
1. Fully Observable (all exits are known, and all piece and board numbers and locations measurable)
2. Deterministic (There is no probability in the problem; outcomes of actions are certain)
3. Sequential (The benefit of a given move )
4. Static (There is no time factor in the actual problem; the game state/environment remains equal whilst actions are being decided)
5. Discrete (Finite number of outcomes, either all pieces are exited or not)

The problem was interpreted as a search problem on a directed graph of possible game states, reachable by playing different actions.
- States: the exact number and positions of each player piece and block.
- Actions: Move, Jump, and Exit (a move is assumedly always possible as per project specifications). All actions are of equal cost.
- Goal tests: Goal state achieved if no player pieces remaining on board, and has not been achieved otherwise.
- Path costs: Calculated as total no. of actions made (as all actions costed uniformly). An optimal path is one that reaches the goal with least possible cost from an origin state.

#### *What search algorithm does your program use to solve this problem, and why did you choose this algorithm?
(You could comment on the algorithm’s efficiency, completeness, and optimality. You could explain any
heuristics you may have developed to inform your search, including commenting on their admissibility.)*

## Algorithmic Approach (Answers Q2)

### Heuristic

Our heuristic was derived from a relaxed version of the search problem, which allows piece(s) to jump freely, even if there is no block/piece to jump over (an empty space to land still had to be available). In this version, pieces would not need to converge in attempt to jump over each other and reduce path costs, as pieces can reach the goal independently, at maximal speed, at their own independent minimal cost.

#### Explanation
`Dijkstra_heuristic` evaluates the total minimal cost to exit all pieces if they move independently under these relaxed conditions. The board with the blocks (but not pieces) is preprocessed using a Dijkstra graph search algorithm with a priority queue to map the minimum cost of exiting for a piece at any location.

#### Benefits
Firstly, the heuristic is admissible.
##### PROOF
Let h:G->N, h(x) denote the value of the heuristic applied to a state x, for some x \in \G, the set of all game states.
Let o:G->N, o(x) denote the exact cost to traverse to goal for a state x.
P(1): admissible for just prior to solution.
  o(x) = 1 (one action away)
  h(x) = 1 (one action away in relaxed problem too)
  Hence P(1).
Inductive:
  Let x' + action = x
  P(x): h(x) <= o(x)
  P(x'): h(x') <= o(x')
  Must show: P(x) ==> P(x') always
  Given: h(x) <= o(x) (1)
  Use (1) -- h(x) <= o(x) + 1
  So h(x) <= o(x')  
  Just show: h(x') <= h(x)
  Well x' to x is either a jump, move, or exit.
  EXIT // one less piece, guarantees less 1.
  so h(x') - 1 = h(x)
  MOVE // h(position_x) = minimum cost to exit x
  h(x') = sum(h(position_x') for x' in pieces)
  So h(x) = h(position_x') ... + h(position_x' + m)
  To prove: h_p(x'+ m) >= h_p(x')






- *Consistent*: **requires h(x) >= d(x,y) + h(y)... CHECK? (i.e. there is no gain to moving in expensive directions)**

**EXAMPLE EVALUATION WITH A FANCY LATEX MARKUP PIC TO IMPRESS??**

The heuristic was optimised to reduce space/time complexity by memoizing the first evaluation (as the position of goals and blocks are static), allowing for constant O(m) time/space computation, where m is the number of player pieces. Given m is small, it is effectively O(1) time/space complexity to evaluate any node.

#### Limitations
The nature of the relaxed problem allows for jumping - thus, the preferred action for movement where permissible is jumping, and this is valued accordingly by the heuristic. For dense boards this heuristic can find optimal jumping paths and weight them as the best action to take, which yields strong performance. However, for sparse graphs with few jumping prospects, the heuristic evaluates the board as 'flat', where movement actions seem to be of little value. **INSERT PICTURE/REFERENCE TO ABOVE** Consequently, sparser configurations can degenerate evaluations to uniform-cost search, which fails to reduce branching factor.

Furthermore, the heuristic assumes independent piece movement (as per the nature of the relaxed problem). Thus, the heuristic fails to value movement that allows 'leapfrogging' piece movements (where a pair of pieces jump over each other), a move that requires pieces make moves conditional on other pieces' positioning.

As leapfrogging is likelier to occur on sparse boards, overall the heuristic significantly underestimates true solution cost in sparse graphs due to its simplifying assumptions.

### Search algorithm: IDA*

Iterative Deepening A* (IDA*) was used to search the game tree. States were evaluated as f(n) = g(n) + h(n), where g(n) was path cost to reach it, and h(n) a heuristic estimate of the cost to achieve the goal from the position. A threhold is maintained that defines the cut between the expanded and unexpanded nodes. At each deepening, leaf nodes are expanded, and the least-cost new leaf's total cost defines the new threshold. This cycle continues until the goal is found, or all states exhausted.

#### Motivating factors
_Why did we choose IDA* other than our ADS fanboyism? Why does A* suck? Why not ID? Why not UCS?_

#### Theoretical space/time complexity
Unlike A*, does not maintain a large set of unvisited states (which being unordered is O(size) time/space-complex to search). Instead nodes/states are stored in a tree structure, where child nodes are game states descending from a parent game state. Ultimately, both approaches are memory-expensive (O(b^d)) in the worst-case), and IDA* by virtue of design requires nodes be revisited recursively to generate new nodes. To circumvent this, a tranposition table/set was utilised (**see below**).

#### Completeness
Assuming an origin state has a valid solution, IDA* explores all possible paths and hence is guaranteed to expand the goal state. **SOURCE/PROOF?**

#### Optimality
If the heuristic function used is admissible, then the least-cost path found using IDA* is optimal. **SOURCE/PROOF?**

#### Optimisations
As a state is fully-observable, a Transposition Table (TT) was used to efficiently memoize the unique states (and state evaluations) encountered during a search. States were indexed with a memory-efficient zero-collision hash. During the search, newly expanded nodes that were previously generated were trimmed if they were of equal or worse total cost than previous encounters. This not only prevented un-necessary re-searching of identical subtrees, but ensured any stored state was the most-optimally reached so far.
 **WE NEED MAGIC'S COUNT/RATE OF TRIMMING TO GET AN IDEA OF TIME/SPACE COMPLEXITY REDUCTION?**

#### *What features of the problem and your program’s input impact your program’s time and space requirements?
(You might discuss the branching factor and depth of your search tree, and explain any other features of the
input which affect the time and space complexity of your algorithm.)*

## Effectiveness of Approach (Answers Q3)

### Asymptotic Time-Space Complexity Analysis
- **Use valgrind for space, it's better than getsizeof macro 4sure, infer a good O() and compare to theoretical esimates**
- **Maybe graph # generated vs bash time for test files, infer a good O() cost and compare to theoretical estimates**

### Depth (does it explore beyond optimal depth?)
The path cost to achieve a goal state can vary from 1 to over 30 steps in some states, particularly where more pieces are used, the result being that the game tree has high average depth. Furthermore, a state can be reached repeatedly by 'backtracking', only adding to the depth and diluting the tree with repetition of suboptimal paths.

### Branching (does it get dense? Is it wasting time on expansions?)
In the worst case, when a state has a few, sparsely spread blocks, a game state can have up to 24 possible actions - movement in 6 directions for 4 pieces. Due to this, the problem tree has potental to be highly dense, which encroaches on time complexity and space complexity.

Some optimisations were implemented to counter excessive depth and branching.

1. The algorithm was coded to always exit pieces if exit actions were possible at any stage, reducing branching in the endgame *SUBTLE REFERENCE* to some extent.

2. Transposition tables eliminated repetition 'down the branch' and 'across the branch'. This is to say that the same state was never expanded twice, and that only the most optimally reached instance is used in the search problem.

Ultimately, runtime data indicates an average branching factor of about 8.5-9.5 generated children per parent. **MAY NEED FURTHER EVIDENCE TO CONCLUDE THAT THIS IS AN IMPROVEMENT FROM THE STATUS QUO**
The data suggests that our trimming optimisations only marginally decrease the branching factor. This is expected; our algorithms evaluates children post-creation.



What does the problem contribute to this issue?
Does the input or its features impact this?
What features of the problem allowed us to reduce branching?
- **Measure branching factor with a tree sweep post-generation TICK - average b is about 9-10 (10 for harder problems), average depth varies b/t 3 for easy, and 7-8 for difficult. Given difficult problems actually have depth 20-30, this is a a strong reduction in net generation - reduced from O(b^{d_optimal}) to O(b^{d_optimal/3})**
