# CSC3022F - RL Assignment 2
# May 2021
# This file contains the generateAnimat function that generates an animation of 2D array data.
# The function can also generate an animated gif so if you are having trouble getting things to work in your terminal,
# you can view your results from the generated file.
# The 'col' parameters make assumptions about the size of the rewards you give your agents. You may need to change their values to generate an animation with 
# clearly identifiable start and end states.
# The final frame of the animation showcases the supplied optimal policy as it would be executed by the agent on the given environment.
# The function also assumes that the last record represents the iteration/epoch where, in the case of Value Iteration, convergence was DETECTED and
# in the case of Q-Learning, the last record is the last epoch on the learning algorithm

# Don't forget to turn off interpolation when viewing these animations or else each cell will not be easily identifiable.

# Import packages
import animatplot as amp
import matplotlib.pyplot as plt
import numpy as np

def generateAnimat(records: [[float]], start_state: (float, float), end_state: (float, float), 
	mines: [(float, float)] = [], opt_pol: [(float, float)] = [], start_val: int = 0, end_val: int = 255, mine_val: int = 254, opt_val: int = 50,
	fps: int = 1, vmin=0, vmax=255, generate_gif: bool = False, filename: str = 'animat', just_vals: bool = False):

	fig, ax = plt.subplots()

	def animate(i):

		ax.set_xlabel('X')
		ax.set_ylabel('Y')

		is_last_frame = i == len(records) - 1

		if not just_vals:
			# Set start state col
			records[i][start_state[0]][start_state[1]] = start_val
			# Set end state col
			records[i][end_state[0]][end_state[1]] = end_val
			# Set mine col
			for mine in mines:
				records[i][mine[0]][mine[1]] = mine_val

			# Setup the final frame of the animation
			if is_last_frame:
				for j in range(len(records[i])): # Set all 'pixels' to a value of zero
					for k in range(len(records[i][j])):
						records[i][j][k] = 0
			
				for state in opt_pol:
					records[i][state[0]][state[1]] = opt_val

		# Generate the pix map
		ax.imshow(records[i], interpolation='none', cmap='jet', vmin=vmin, vmax=vmax)

		# Put values on p[i]ix map
		for j in range(len(records[i])):
			for k in range(len(records[i][j])):

				text=[str(round(records[i][j][k],3))] if not is_last_frame else []

				# Check if state is start state,
				if j == start_state[0] and k == start_state[1]:
					text = ['start'] + text if just_vals else ['start']
				elif j == end_state[0] and k == end_state[1]:
					text = ['end'] + text if just_vals else ['end']
				else:
					for mine in mines:
						if j == mine[0] and k == mine[1]:
							text = ['landmine'] + text if just_vals else ['landmine']

				if is_last_frame:
					for si in range(len(opt_pol)):
						if j == opt_pol[si][1] and k == opt_pol[si][0]:
							text.append('\nS_' + str(si))
				ax.text(k, j, '\n'.join(text), ha='center', va='center', color='w')
			



	blocks = amp.blocks.Nuke(animate, length=len(records), ax=ax) # Required call to build our animation
	timeline = np.arange(len(records))
	anim = amp.Animation([blocks], amp.Timeline(timeline, fps=fps))  # Builds the Animation
	anim.controls()  # Gives us a pause and start button
	
	if generate_gif:  # Write animation to file if generate_gif is True
		anim.save_gif(filename)

	return anim, fig, ax
	