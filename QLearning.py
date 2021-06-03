from utils import extract_args, init_states, init_mines,determine_possible_actions
import sys


def init_rewards(width, height, mine_locs, end_pt, grid_world, possible_actions):
    rewards = {}
    for position in possible_actions:
        rewards[position] = [0,0,0,0]

        x = position[1]
        y = position[0]

        for action in  possible_actions[position]:
            next_move = None
            if(action == "U"):
                next_move = (y-1,x)
                if(next_move in grid_world):
                    rewards[position][0] = -1
                if(next_move in mine_locs):
                    rewards[position][0] = -100
                if(next_move == end_pt):
                    rewards[position][0] = 100




            if(action == "D"):
                next_move = (y+1,x)
                if(next_move in grid_world):
                    rewards[position][1] = -1
                if(next_move in mine_locs):
                    rewards[position][1] = -100
                if(next_move == end_pt):
                    rewards[position][1] = 100


            if(action == "L"):
                next_move = (y,x-1)
                if(next_move in grid_world):
                    rewards[position][2] = -1
                if(next_move in mine_locs):
                    rewards[position][2] = -100
                if(next_move == end_pt):
                    rewards[position][2] = 100

    
            if(action == "R"):
                next_move = (y,x+1)
                if(next_move in grid_world):
                    rewards[position][3] = -1
                if(next_move in mine_locs):
                    rewards[position][3] = -100
                if(next_move == end_pt):
                    rewards[position][3] = 100
    
    for position in rewards:
        print(f"{position} : {rewards[position]}")
    

    return rewards
            
            



if __name__ == "__main__":

    #get the arguments
    width, height, start_pt, end_pt, k, gamma, learning, generations = extract_args(sys.argv)
    print(extract_args(sys.argv))
    grid_world = init_states(width, height)
    mine_locs = init_mines(k, start_pt, end_pt, width, height)
    possible_actions = determine_possible_actions(width, height, mine_locs)
    print("Grid World 48-H#: ")
    print(grid_world, end="\n\n")
    print("Possible actions for each location:")
    print(possible_actions, end="\n\n")
    print(f"Start Position {start_pt}")
    print(f"End Position {end_pt}", end="\n\n")
    print(f"Number of Mines:  {k}")
    print("Mines are initialised at the following locations: ")
    print(mine_locs, end="\n\n")

    print("R table ")
    action_rewards = init_rewards(width, height, mine_locs, end_pt, grid_world, possible_actions)

    









