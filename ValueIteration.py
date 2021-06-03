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
            states.append((y,x))
        #states.append(row)

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

        coord = (y_pos, x_pos)

        #check that the points are equal and then generate a place until they are not
        if(coord == start or coord == end or coord in mine_locs):
            while (coord == start or coord == end or coord in mine_locs):
                x_pos = randint(0, width-1)
                y_pos = randint(0, height-1)
                coord = (y_pos, x_pos)
        
        mine_locs.append(coord)
    
    return mine_locs

def init_rewards(width, height, mine_locs, end_pt ):
    rewards = []
    for y in range(height):
        reward_row = []
        for x in range(width):
            reward_row.append(0)
        rewards.append(reward_row)

    print(f"Intial reward values before mines and end:\n {np.array(rewards)}")
    #setting values for mines 
    for mine in mine_locs:
        # mine loc is <y, x>
        print(f"x:{mine[1]}, y:{mine[0]}")
        rewards[mine[0]][mine[1]] = -1
    
    rewards[end_pt[0]][end_pt[1]] = 1
    
    print(f"Intial reward values after mines and end:\n {np.array(rewards)}")
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
            coord = (y, x)
            actions = [0,0,0,0] # assume terminal state
            if coord not in mine_locs and coord != end_pt: #should not be able to move out of terminal state if it is a mine or end 
                
                if(y != 0 and (y-1,x) not in mine_locs ):
                    actions[0] = 1
                if(y != height-1 and (y+1,x) not in mine_locs):
                    actions[1] = 1
                if(x != 0 and (y,x-1) not in mine_locs):
                    actions[2] = 1
                if(x != width-1 and (y,x+1) not in mine_locs):
                    actions[3] = 1
            actions_row.append(actions)
        actions_list.append(actions_row)
    return actions_list

def get_final_action_arr(position, next_position):
    action_arr = []
    if (next_position[0]  == position[0]-1):
        action_arr = [1, 0, 0, 0]
    if (next_position[0]  == position[0]+1):
        action_arr = [0, 1, 0, 0]
    if (next_position[1]  == position[1]-1):
        action_arr = [0, 0, 1, 0]
    if (next_position[1]  == position[1]+1):
        action_arr = [0, 0, 0, 1]
    return action_arr

def determine_possible_actions(width, height, mine_locs):
    actions = {}
    for y in range (height):
        for x in range(width):
            coord = (y, x)
            legal_moves = []
            if(coord not in mine_locs):
                if (y < height-1):
                    legal_moves.append("D")
                if (y > 0):
                    legal_moves.append("U")
                if (x < width-1):
                    legal_moves.append("R")
                if (x > 0):
                    legal_moves.append("L")
            
                actions[coord] = tuple(legal_moves)
    
    return actions
                
                
    

def iterate(width, height, mine_locs, start_pt, end_pt, possible_actions, initial_rewards, gamma, grid_world):


    states = []

    #initial V 
    V = {}
    policy = {}
    for position in grid_world:
        V[position]  = initial_rewards[position[0]][position[1]]
        if(position not in mine_locs):
            policy[position] = np.random.choice(possible_actions[position])
    
    # states.append(V)
    # policy ={start_pt: possible_actions[start_pt]}

    # print(f"POLICY: {policy}")


    while True :
        
        #use some difference factor
        difference = 0
        for position in grid_world:
            if position in policy:
               
                new_value = 0
                old_value = V[position]

                y = position[0]
                x = position[1]
                
    
                for action in possible_actions[position]:
                    next_move = None
                    if(action == "U"):
                        next_move = (y-1,x)
                    if(action == "D"):
                        next_move = (y+1,x)
                    if(action == "L"):
                        next_move = (y,x-1)
                    if(action == "R"):
                        next_move = (y,x+1)
        
                    discount =  gamma*(V[next_move])
                    v = initial_rewards[position[0]][position[1]] + discount
               

                    if v > new_value:
                 
                        new_value = v
                        policy[position] = action
                        
        
                V[position] = new_value

                difference = max(difference, np.abs(old_value-new_value))
        if difference == 0:
            break
    
    return policy
                    




    
    
            
            










if __name__ == "__main__":

    #get the arguments
    width, height, start_pt, end_pt, k, gamma = extract_args(sys.argv)
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
    initial_rewards = init_rewards(width, height, mine_locs, end_pt)
    

    print(iterate(width, height, mine_locs,start_pt, end_pt, possible_actions, initial_rewards, gamma, grid_world))

    


  
    