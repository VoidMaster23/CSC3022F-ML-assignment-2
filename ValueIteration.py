import  sys
from utils import extract_args
import numpy as np
from random import randint

def init_states(width, height):
    """
    Function to initialise the 2D array
    
    Arguments: 
        width (int): number of grid columns
        height (int): number of grid rows
    
    Returns:
        initalStates (array): numpy array of shape (height, width)
    """

    states = []
    
    for y in range(height):
        row = []
        for x in range(width):
            row.append((y,x))
        states.append(row)

    return states
    
def init_mines(k, start, end, width, height):
    """
    Function to initialise the location of the mines 

    Arguments: 
        k (int) : number of landmines
        start Tuple(x, y): the starting point for the agent
        end  Tuple(x,y): end point for the agent
        width (int): width of the envionment
        height (int): height of the enviroment
    
    Returns:
        mine_locs (array): numpy array of shape [k, ] 
    """
    mine_locs = []
    for i in range(k):
        x_pos = randint(0, width-1)
        y_pos = randint(0, height-1)

        coord = (x_pos, y_pos)

        #check that the points are equal and then generate a place until they are not
        if(coord == start or coord == end ):
            while (coord == start or coord == end):
                x_pos = randint(0, width-1)
                y_pos = randint(0, height-1)
                coord = (x_pos, y_pos)
        
        mine_locs.append(coord)
    
    return mine_locs

def init_rewards(width, height, mine_locs, end_pt ):
    rewards = []
    for y in range(height):
        reward_row = []
        for x in range(width):
            reward_row.append(-1)
        rewards.append(reward_row)

    print(f"Intial reward values before mines and end: {rewards}")
    #setting values for mines 
    for mine in mine_locs:
        # mine loc is <x, y>
        print(f"x:{mine[0]}, y:{mine[1]}")
        rewards[mine[1]][mine[0]] = -100
    
    rewards[end_pt[1]][end_pt[0]] = 100
    
    print(f"Intial reward values after mines and end: {rewards}")
    return rewards

def get_possible_actions_list(width, height, mine_locs, end_pt):
    """
    Function to determine the possible actions available for each state

    Represents an available action as  [UP, DOWN, LEFT, RIGHT] where the presence of a number is given by a binary value ,
     1 meaning the action is valid for that state and 0 meaning that it is not
    """
    actions_list = []
    for y in range(height):
        actions_row = []
        for x in range(width):
            coord = (x, y)
            actions = [0,0,0,0] # assume terminal state
            if coord not in mine_locs and coord != end_pt: #should not be able to move out of terminal state if it is a mine or end 
                if(y != 0):
                    actions[0] = 1
                if(y != height-1):
                    actions[1] = 1
                if(x != 0):
                    actions[2] = 1
                if(x != width-1):
                    actions[3] = 1
            actions_row.append(actions)
        actions_list.append(actions_row)
    return actions_list

            






if __name__ == "__main__":

    #get the arguments
    width, height, start_pt, end_pt, k, gamma = extract_args(sys.argv)
    initalStates = init_states(width, height)
    mine_locs = init_mines(k, start_pt, end_pt, width, height)
    possible_actions = get_possible_actions_list(width, height, mine_locs, end_pt)
    print("Grid World 48-H#: ")
    print(initalStates, end="\n\n")
    print("Possible actions for each location:")
    print(possible_actions, end="\n\n")
    print(f"Start Position {start_pt}")
    print(f"End Position {end_pt}", end="\n\n")
    print(f"Number of Mines:  {k}")
    print("Mines are initialised at the following locations: ")
    print(mine_locs, end="\n\n")
    initial_rewards = init_rewards(width, height, mine_locs, end_pt)

    


  
    