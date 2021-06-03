from utils import extract_args, init_states, init_mines,determine_possible_actions
import sys
import numpy as np
import random
from Animate import generateAnimat
import matplotlib.pyplot as plt
import copy

def init_R_Q(width, height, mine_locs, end_pt, grid_world, possible_actions):
    rewards = {}
    initial_Q = {} 
    for position in grid_world:
        initial_Q[position] = [0,0, 0,0]
        rewards[position] = [0,0,0,0]

        x = position[1]
        y = position[0]

        if(position in possible_actions):
            for action in  possible_actions[position]:
                next_move = None
                if(action == "U"):
                    next_move = (y-1,x)
                    if(next_move in possible_actions):
                        rewards[position][0] = 0
                    if(next_move in mine_locs):
                        rewards[position][0] = -100
                    if(next_move == end_pt):
                        rewards[position][0] = 100




                if(action == "D"):
                    next_move = (y+1,x)
                    if(next_move in grid_world):
                        rewards[position][1] = 0
                    if(next_move in mine_locs):
                        rewards[position][1] = -100
                    if(next_move == end_pt):
                        rewards[position][1] = 100


                if(action == "L"):
                    next_move = (y,x-1)
                    if(next_move in grid_world):
                        rewards[position][2] = 0
                    if(next_move in mine_locs):
                        rewards[position][2] = -100
                    if(next_move == end_pt):
                        rewards[position][2] = 100

        
                if(action == "R"):
                    next_move = (y,x+1)
                    if(next_move in grid_world):
                        rewards[position][3] = 0
                    if(next_move in mine_locs):
                        rewards[position][3] = -100
                    if(next_move == end_pt):
                        rewards[position][3] = 100
        
    
    for position in rewards:
        print(f"{position} : {rewards[position]}")
    

    return rewards, initial_Q
            

def run_q(generations,gamma ,mine_locs, learning_rate, action_rewards,initial_Q, grid_world, end_pt): 

    finished = False
    generation_rewards  = []     

    

    #for each generationn
    q_table = initial_Q.copy()
    q_prev = initial_Q.copy()


    # records = [q_prev]
    print("RECORDS")
 
    records  = [copy.deepcopy(q_table)]
    iteration_count = 0
    for generation in range(generations):
        records.append(q_prev.copy())

        # new_state = initial_Q
        converged = False
        total_rewards = 0

        #set the random current state
        position = random.choice(list(possible_actions.keys()))

        while position != end_pt :

            y = position[0]
            x = position[1]
            
            if position in mine_locs or position == end_pt:
                break


            #random action
            action = None

            action = np.random.choice(possible_actions[position])

            #find out where to go
            next_move = None
            move_index = None
            if(action == "U"):
                next_move = (y-1,x)
                move_index = 0
                

            if(action == "D"):
                next_move = (y+1,x)
                move_index = 1

            if(action == "L"):
                next_move = (y,x-1)
                move_index = 2

            if(action == "R"):
                next_move = (y,x+1)
                move_index = 3

            old_value = q_table[position][move_index]

            max_move_q = max(q_table[next_move])
            q_table[position][move_index] = old_value + learning_rate*(action_rewards[position][move_index] + gamma*max_move_q - old_value)
            q_prev = q_table.copy()
            # new_rec = q_table.copy()
            position = next_move
        records.append(copy.deepcopy(q_table))   
        # print(q_prev)
        
            
        
        iteration_count += 1
    
    for position in action_rewards:
        print(f"{position} : {q_table[position]}")
    

    return records, q_table
        

def generate_opt_pol(final_q, start_pt, end_pt):
    opt_pol = [start_pt]
    point = start_pt
    #opt_pol.append(point)
    # for point in final_q:
    while point != end_pt:
        
        y = point[0]
        x = point[1]

        
        row_q = final_q[point]
        if row_q != [0,0,0,0]:
            max_index = row_q.index(max(row_q))

            # print(f'rows: {row_q}, max_index: {max_index}')

            if(max_index == 0):
                
                coord = (y-1,x)
                if(coord in final_q):
                    point = coord

            if(max_index == 1):
                coord = (y+1,x)
                if(coord in final_q):
                    point = coord
            if(max_index == 2):
                coord = (y,x-1)
                if(coord in final_q):
                    point = coord
            if(max_index == 3):
                coord = (y,x+1)
                if(coord in final_q):
                    point = coord
            
            opt_pol.append(point)
        else:
            opt_pol.append(point)
            # print(opt_pol)
            break
        
    return opt_pol

def generate_records(raw_records, width, height):

    records = []
    for raw_record in raw_records:
        record = []
        for y in range(height):
            row = []
            for x in range(width):
                coord = (y, x)
                row.append(max(raw_record[coord]))
                
            record.append(row)
        records.append(record)
    
    return records


if __name__ == "__main__":

    #get the arguments
    width, height, start_pt, end_pt, k, gamma, learning_rate, generations = extract_args(sys.argv)
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
    action_rewards, initial_Q = init_R_Q(width, height, mine_locs, end_pt, grid_world, possible_actions)

    print("\n Initial Q:")
    for position in action_rewards:
        print(f"{position} : {initial_Q[position]}")
    
    print()
    print("Final Q table: ")
    raw_records, final_q = run_q(generations,gamma ,mine_locs, learning_rate, action_rewards,initial_Q, grid_world, end_pt)

    records = generate_records(raw_records, width, height)


    print(f"Optimal Policy from {start_pt} to {end_pt} :")
    opt_policy = generate_opt_pol(final_q, start_pt, end_pt)

    print(opt_policy)  

    print("\n GENERATING OUTPUT")
    anim, fig, ax = generateAnimat(records, start_pt, end_pt, mines=mine_locs, opt_pol=opt_policy, start_val=0, end_val=100, mine_val=-100, just_vals=False, generate_gif=True, filename = 'q_learn_results')
    plt.show()










