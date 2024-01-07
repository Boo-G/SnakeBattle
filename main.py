# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Slitherin",  
        "color": "#888888",  
        "head": "silly",  
        "tail": "bonhomme",  
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

# given a game_state of my_head and a move of right, left, up or down.
def findNextMovePosition(my_head, move):
    if move == "right":
        return {"x":my_head["x"]+1,"y":my_head["y"]}
    
    elif move == "left":
        return {"x":my_head["x"]-1,"y":my_head["y"]}
    
    elif move == "up":
        return {"x":my_head["x"],"y":my_head["y"]+1}
    
    elif move == "down":
        return {"x":my_head["x"],"y":my_head["y"]-1}


# find the distance between the start and end
def findDistance(start,end): 
    return abs(start["x"] - end["x"]) + abs(start["y"] - end["y"])



# return a dictionary of the closest food relative to the snake head
def closestFood(my_head,allFood):
    shortest = 0
    closeFood = {}

    for food in allFood:
        if findDistance(my_head,food) < shortest:
            shortest = findDistance(my_head,food)
            closeFood = food
        
    return closeFood


# return a move that gets me closer to the selected food
def myMove(safe_moves, my_head, closeFood):
    distance = 100
    finalMove  = ""
    for move in safe_moves:
        if findDistance(findNextMovePosition(my_head,move),closeFood) < distance:
            distance = findDistance(findNextMovePosition(my_head,move),closeFood)
            finalMove = move
    
    return finalMove






# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head {"x": 0, "y": 0}
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["x"]  == 0:
        is_move_safe["left"] = False

    elif my_head["x"] == board_width - 1:
        is_move_safe["right"] = False

    elif my_head["y"] == 0:
        is_move_safe["down"] = False

    elif my_head["y"] == board_height - 1:
        is_move_safe["up"] = False

    # Step 2 - Prevent your Battlesnake from colliding with itself
        
    # technically pointless as its done in step 3
    my_body = game_state['you']['body'] # Example for body: [{"x": 0, "y": 0}, ..., {"x": 2, "y": 0}]

    for move in is_move_safe.keys():
        if findNextMovePosition(my_head,move) in my_body[1:]:
                is_move_safe[move] = False


    # Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']

    for opponet in opponents:
        for move in is_move_safe.keys():
            if findNextMovePosition(my_head,move) in opponet["body"]:
                    is_move_safe[move] = False


    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items(): # [4,3,2,1]  enumerate move = 0, isSafe = 4
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down",}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']

    next_move = myMove(safe_moves, my_head, closestFood(my_head,food))

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
