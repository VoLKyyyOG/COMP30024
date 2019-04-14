Game Implementation
========
### TODO:
`game_over` flag when a player has `NO_EXITED_PIECE = 4`   

`is_eliminated` flag when a player has been eliminated

### Current progress
80 turns at 0.078 game total time using Agent_Random

### Program Flow
The player class holds `colour`, `state`, and `goal`. The `state` is in format `{color: [{piece coordinates}, no_pieces, no_exited_pieces]}`

When `action()` is called:
1. Our agent's state is given by `player.state[player.colour]`
2. For each coordinate in agent's state:
    - Check which strategy we are using (early game, mid game, end game)
    - if strategy is early game:
        - choose a random action in possible_actions
        - FOR NOW. LATER WE CAN USE BOOK LEARNING TO CHOOSE
    - if strategy is mid game:
        - use MP_MIX
    - if strategy is end game:
        - use minimax
   
### Dependencies
`moves.py`, `agent_logic.py`

when either `MP-MIX` OR `minimax` is called in `agent_logic()`, they can be imported functions from other `.py` files with their own dependencies.
