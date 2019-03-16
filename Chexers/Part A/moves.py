# Returns goals given player colour
def find_goal(player, data):
    # Initialise goals
    from collections import defaultdict
    goals = defaultdict(list)
    goals["red"].append([[3,r] for r in range(-3, 1)])
    goals["blue"].append([[-3,0],[-2,1],[-1,2],[0,3]])
    goals["green"].append([[q,3] for q in range(-3, 1)])

    # Default player goal
    player_goal = goals[player][0]

    # Check if goal not blocked by piece
    player_goal = [i for i in player_goal if i not in data["blocks"]]

    return player_goal

# Possible moves from current location
def possible_moves(data, player_goal):
    player_pos = data["pieces"]
    block_pos = data["blocks"]
    
    for i in player_pos:
        print("Player coordinate: ",i) 
        valid_hexes = adj_hex(i)

        possible_moves = move(valid_hexes, data)
        possible_jumps = jump(valid_hexes, data)
        possible_exits = exit_move(i, player_goal)
        print("**********************************************************")

        # check if there is block
        # if no block:
            # return move()
        # if block:
            # skippable?
                # return jump()
        # if exit:
            # return exit()
        

def adj_hex(coordinate):
    # Taken from the test generator script
    valid_coordinates = [[-3, 0], [-3, 1], [-3, 2], [-3, 3], 
                        [-2, -1], [-2, 0], [-2, 1], [-2, 2], [-2, 3], 
                        [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2], [-1, 3], 
                        [0, -3], [0, -2], [0, -1], [0, 0], [0, 1], [0, 2], [0, 3], 
                        [1, -3], [1, -2], [1, -1], [1, 0], [1, 1], [1, 2], 
                        [2, -3], [2, -2], [2, -1], [2, 0], [2, 1], 
                        [3, -3], [3, -2], [3, -1], [3, 0]]
    
    # https://www.redblobgames.com/grids/hexagons/#neighbors-axial
    qr1 = [coordinate[0] + 1, coordinate[1]]
    qr2 = [coordinate[0] + 1, coordinate[1] - 1]
    qr3 = [coordinate[0], coordinate[1] - 1]
    qr4 = [coordinate[0] - 1, coordinate[1]]
    qr5 = [coordinate[0] - 1, coordinate[1] + 1]
    qr6 = [coordinate[0], coordinate[1] + 1]
    hexes = [qr1,qr2,qr3,qr4,qr5,qr6]

    # Checks if the hexes above are valid (within the board)
    valid_hexes = [i for i in [j for j in hexes] if i in valid_coordinates]

    print("Adjacent hexes at:", valid_hexes)

    return valid_hexes

def move(valid_hexes, data):
    possible_moves = [i for i in valid_hexes if i not in data["blocks"]]

    print("Possible Move Action to:",possible_moves)

    return possible_moves

def jump(valid_hexes, data):
    possible_jumps = [i for i in valid_hexes if i in data["blocks"] or i in data["pieces"]]

    print("Possible Jump Action to:",possible_jumps)

    return possible_jumps

def exit_move(coordinate, player_goal):
    possible_exits = coordinate in player_goal

    print("Exit Possible? ", possible_exits)

    return possible_exits