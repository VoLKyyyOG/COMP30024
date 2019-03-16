# def move():
#     from location, if move valid:
#         return piece new coordinate
#
# def jump():
#     from location, if jump valid:
#     return piece new coordinate
#
# def exit():
#     from location, if exit valid:
#     return REMOVE PIECE

from classes import *

# Returns goals given player colour
def find_goal(player, data):
    # Initialise goals
    from collections import defaultdict
    goals = defaultdict(list)
    goals["red"].append([[3,r] for r in range(-3, 1)])
    goals["blue"].append([[-3,0],[-2,1],[-1,2],[0,3]])
    goals["green"].append([[q,3] for q in range(-3, 1)])

    # SCAFFOLDING: just go for this goal for now, adjust it later
    player_goal = goals[player][0]

    # Check if goal not blocked by piece
    player_goal = [i for i in player_goal if i not in data["blocks"]]

    return player_goal

# Possible moves from current location
def possible_moves(data):
    player_pos = data["pieces"]
    block_pos = data["blocks"]

    for i in player_pos:
        print("Player coordinate: ", i) #i is coordinate to be fed into adj_hex

        adj_hex(i)
        print("**********************************************************")
        # add 1 to surrounding space
        # check if there is block
        # if no block:
            # return move
        # if block:
            # skippable?
                # return jump

def adj_hex(coordinate):
    valid_coordinates = [[q, r] for q in range(-3,4) for r in range(-3,4)]
    qr1 = [coordinate[0] + 1, coordinate[1]]
    qr2 = [coordinate[0] + 1, coordinate[1] - 1]
    qr3 = [coordinate[0], coordinate[1] - 1]
    qr4 = [coordinate[0] - 1, coordinate[1]]
    qr5 = [coordinate[0] - 1, coordinate[1] + 1]
    qr6 = [coordinate[0], coordinate[1] + 1]
    adj_hexes = [qr1,qr2,qr3,qr4,qr5,qr6]
    print([i for i in [j for j in adj_hexes] if i in valid_coordinates])
