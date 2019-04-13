Game Implementation
========
### TODO:
In `update(self, colour, action)`, if a piece is captured then:
```python
player = self.state[colour] # a set of coordinates for the given player colour
current = action[1][0]
destination = action[1][1]

if action[0] == "JUMP":
    jumped_piece = function find_middile_hex() # coordinate of the jumped piece
    if jumped_piece in player[PIECE_COORD]:
        player.remove(current)
        player.add(destination)
    else: # we have captured a piece
        opponent_colours = [i for i in self.state.keys() if i != colour]
        for colour in opponent_colours:
            opponent = self.state[colour]
            if jumped_piece in opponent[PIECE_COORD]:
                opponent[NO_PIECES] -= 1
                opponent[PIECE_COORD].remove(jumped_piece)
                player.add(jumped_piece)
                player[NO_PIECES] += 1
                break
```



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
