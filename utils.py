# Utils.py
# Contains common functions for the assignment
# Author: Edson Shivuri (SHVNKA005)

from random import randint

def extract_args(args):
    """
    Function to extract arguments from command line 

    Arguments:
        args (list): [] list of arguments from the command line
    
    Returns:
        width (int): width of the envionment
        height (int): height of the enviroment
        start_Xpos (int): starting x position of the agent
        start_Ypos (int): starting y position of the agent
        end_Xpos (int): ending x position of the agent
        end_Ypos (int): ending y position of the agent
        num_mines (int): number of landmines
        gamma (float): discount factor
    """
    print(args[0])
    #get the env dimensions
    width = int(args[1])
    height = int(args[2])


    #get the positions 
    start_Ypos = None
    start_Xpos = None

    end_Ypos = None
    end_Xpos = None
    if("-start" in args and "-end" in args ):
        s_ind = args.index("-start")
        start_Xpos = int(args[s_ind+1])
        start_Ypos = int(args[s_ind+2])

        e_ind = args.index("end")
        end_Xpos = int(args[e_ind+1])
        end_Ypos = int(args[e_ind+2])
    else:
        print("Start or End Positions not given, randomising both values")
        start_Ypos = randint(0,height-1)
        start_Xpos = randint(0,width-1)

        end_Ypos = randint(0,height-1)
        end_Xpos = randint(0,width-1)

        #check that the points are equal and then generate a place until they are not
        if(start_Ypos == end_Ypos and start_Xpos == end_Ypos ):
            while (start_Ypos == end_Ypos and start_Xpos == end_Xpos):
                end_Ypos = randint(0,height-1)
                end_Xpos = randint(0,width-1)

    #learning rate
    learning = None
    if("-learning" in args):
        learning = float(args[args.index("-learning")])
    else:
        learning = 0.65

    #epochs
    generations = None
    if("-epochs" in args):
        generations = int(args[args.index("-epochs") + 1])
    else: 
        generations = 500

    #get k
    k = None
    if("-k" in args):
        k = int(args[args.index("-k") + 1])
    else:
        k = 3    

    #get gamma
    gamma = None
    if("-gamma" in args):
        gamma = float(args[args.index("-gamma") + 1])
    else:
        gamma = 0.9

    if args[0] == "ValueIteration.py":
        return width, height, (start_Ypos, start_Xpos), (end_Ypos, end_Xpos), k, gamma
    else: 
        return width, height, (start_Ypos, start_Xpos), (end_Ypos, end_Xpos), k, gamma, learning, generations


def init_states(width, height):
    """
    Function to initialise a list of grid tuples
    
    Arguments: 
        width (int): number of grid columns
        height (int): number of grid rows
    
    Returns:
        initalStates (list<Tuple<y,x>>): height*width length list
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

def determine_possible_actions(width, height, mine_locs):
    """
    construct a set of legal actions for each position, excluding the mine locations
    """
    #
    actions = {}
    for y in range (height):
        for x in range(width):
            coord = (y, x) # row, col
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
    

