# CSC3022F - RL Assignment 2
# May 2021
# This file showcases how you use the generateAnimat function using to
# generate an animation that visualizes your RL agents learning process.

# Import packages
import matplotlib.pyplot as plt

from Animate import generateAnimat

if __name__ == '__main__':
	
	# This is just our records data structure, it contains the records of all V(s) for every state s at a given iteration/epoch in your algorithm
	# records[0][1][1] = the Value of grid position (1, 1) at iteration 0
	# This example assumes that the start state = (0, 0) and the end state = (2, 1) and that there are no land mines
	records = [
		[
			[0, 0,  0 ],
			[0, 0, 100]
	 	],
	 	[
	 		[0,   0,  80],
	 		[0,  80, 100]
	 	],
	 	[
	 		[ 0, 64,  80],
	 		[64, 80, 100]
	 	],
	 	[
	 		[51.2, 64,  80],
	 		[  64, 80, 100]
	 	],
	 	[
	 		[51.2, 64,  80],
	 		[  64, 80, 100]
	 	]
	]

	start_state = (0, 0)
	end_state = (2, 1)

	mines = []
	#mines = [(1,1)]  # Uncomment this to check out what mines will look like

	# We don't need a list of mine positions since our example doesn't have any
	opt_pol = [(0,0), (1, 0), (2, 0), (2, 1)] # The above example has multiple valid optimal policies, this is just one of them.


	anim, fig, ax = generateAnimat(records, start_state, end_state, mines=mines, opt_pol=opt_pol, 
		start_val=-10, end_val=100, mine_val=150, just_vals=False, generate_gif=True,
		vmin = -10, vmax = 150)

	plt.show()