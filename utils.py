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
        start_Ypos = randint(0,height)
        start_Xpos = randint(0,width)

        end_Ypos = randint(0,height)
        end_Xpos = randint(0,width)

        #check that the points are equal and then generate a place until they are not
        if(start_Ypos == end_Ypos and start_Xpos == end_Ypos ):
            while (start_Ypos == end_Ypos and start_Xpos == end_Ypos):
                end_Ypos = randint(0,height)
                end_Xpos = randint(0,width)

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
        gamma = 0.65


    return width, height, (start_Xpos, start_Ypos), (end_Xpos, end_Ypos), k, gamma    



    

