import  sys
from utils import extract_args, init_states, init_mines, determine_possible_actions
import numpy as np
from random import randint
import matplotlib.pyplot as plt

from Animate import generateAnimat

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
        rewards[mine[0]][mine[1]] = -100
    
    rewards[end_pt[0]][end_pt[1]] = 100
    
    print(f"Intial reward values after mines and end:\n {np.array(rewards)}")
    return rewards



                
                
    

def iterate(mine_locs,possible_actions, initial_rewards, gamma, grid_world):
    """
    Function to perform value iteration

    Returns:
        records
        policy
    """

    records = []

    #initial Valies and policy
    V = {}
    policy = {}
    for position in grid_world:
        V[position]  = initial_rewards[position[0]][position[1]]
        if(position not in mine_locs):
            policy[position] = np.random.choice(possible_actions[position]) #choose a random starting action for each policy
    
    records.append(V)

    difference = difference = 100
    #loop until the optimum has been found
    while difference > 0.0001:
        difference = 0
        # visit each position in the grid
        # and evaluate actions for each action available ina position
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
        records.append(V.copy()) #save states
    return records,policy
                    

def generate_opt_pol(policy, start_pt, end_pt):
    opt_pol = []
    point = start_pt
    opt_pol.append(point)
    while point != end_pt:
        y = point[0]
        x = point[1]

        
        action = policy[point]

        if(action == "U"):
            point = (y-1,x)
        if(action == "D"):
            point = (y+1,x)
        if(action == "L"):
            point = (y,x-1)
        if(action == "R"):
            point = (y,x+1)
        
        opt_pol.append(point)
    return opt_pol


def generate_records(raw_records, width, height):
    records = []
    for raw_record in raw_records:
        record = []
        for y in range(height):
            row = []
            for x in range(width):
                coord = (y, x)
                row.append(raw_record[coord])
            record.append(row)
        records.append(record)
    
    return records

    
    
    
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
    

    raw_records, raw_policy  = iterate(mine_locs,possible_actions, initial_rewards, gamma, grid_world)
 

    policy = generate_opt_pol(raw_policy, start_pt, end_pt)
    records = generate_records(raw_records, width, height)

    print(f"Optimal Policy from {start_pt} to {end_pt} :")
    print(policy)
    
    anim, fig, ax = generateAnimat(records, start_pt, end_pt, mines=mine_locs, opt_pol=policy, start_val=0, end_val=100, mine_val=-100, just_vals=False, generate_gif=True)
    plt.show()

    


  
    