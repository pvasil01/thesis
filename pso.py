import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import time
np.set_printoptions(suppress=True)

st = time.time()
pst = time.process_time()

# Load the Excel file into a pandas DataFrame
# Extract the NodeID,x, y  in the node_coordinates array 
nodes_df = pd.read_excel("./Deceptive_random/random_nodes_coordinates.xlsx",sheet_name="Sheet1")

node_coordinates = nodes_df[["Node","X", "Y"]].values


# Load the Excel file into a pandas DataFrame
# Extract the IMPORTANT colums C and H  in the jammed_info array 
simulation_60sec_df = pd.read_excel("./Reactive_random/reactive_random_ALL_values.xlsx", sheet_name="fuzzy_(8)",usecols=[2,7])
jammer_x=60.00
jammer_y=-20.00
simulation_60sec_df = simulation_60sec_df.rename(columns={"Unnamed: 2":"Node" , "Unnamed: 7": "Jammed"})

jammed_info = simulation_60sec_df.values


num_particles = 60
num_iterations=24
num_nodes=24

w = 0.65 # Inertia weight
c1 = 1.2 # Cognitive weight
c2 = 1.4 # Social weight

# This function takes the current position of a particle 
# and a list of affected nodes (affected_nodes) and calculates the
# Euclidean distance between the particle and each affected node.
# The largest distance is returned as the fitness value, which
# represents the radius of the minimal covering circle.
# So fitness function is the minimal covering circle
 
#This is the PSO algorithm function.
# Particles are randomly generated withing the  search space , with a 
# random velocity as well ( velocity in X coordinate and Y coordinate of the search 
# space respectively). Those particles influence one another on the way they move , with 
# each particle being a candidate solution to the problem. It is a minimization problem 
# as we are searching for the particle that has the smallest fitness value. The fitness 
# value is obtained by calculating the minimal covering circle around each particle, with 
# that circle containing each and every node in the network that currently records that 
# it is jammed. Hence , the smallest circle is the best solution. Particles are affected 
# by the values explained in notes , but they are mainly guided by their personal best 
# and by the global best alogn with some randomness. 

# The algorithm begins by dividing the data into batches of 24 nodes. Specifically in our tests
# we had a total of 14 batches. Each batch is basically the records of the nodes for a specific 
# period of time ( nodes record their jamming status). Each batch is processed over 24 times before
# a final estimation is made regrding the precise location of the jammer. 
# For each batch , we generate and initialize the particles. Then for 24 times the code goes over 
# all the particles , one-by-one and calculates their minimal covering circle by checking which 
# nodes are jammed or not and adding the relevant ones to the circle. After a particle is done 
# with checking the 24 nodes of the current batch, we check for a personal best and a global best
# and if necessary update those. Then we move to the next particle and do the exact same thing. 
# After it goes over all the particles 24 times, it moves to the next batch and the same
# the set of particles. 
  
# print ( "DATA LOADED ")
def calculate_fitness(jammed_info, node_coordinates, w, c1, c2):
    total_error=0
	# take each batch one-by-one ( agreed that there should be a result for each batch )
	# reset the position, velocity, fitness etc
    for node_batch_index in range(14):
        jam_count=False
        particle_position = np.zeros((num_particles, 2))
        particle_velocity = np.zeros((num_particles, 2))
        particle_current_fitness = np.zeros(num_particles)
        particle_previous_fitness = np.zeros(num_particles)        
        particle_personal_best_position = np.zeros((num_particles, 2))        
        particle_personal_best_fitness = np.full(num_particles, np.inf)        
        global_best_position=np.zeros((1,2))
        global_best_fitness = float('inf')
        
        # regenerate the positions and velocities for the new batch 
        for j in range(num_particles):
             particle_position[j] = np.random.uniform(0,100,2)
             particle_velocity[j] = np.random.uniform(0,100,2)
        max_distance = float('-inf')

		# pick the next batch
        node_batch = jammed_info[node_batch_index*num_nodes : (node_batch_index+1)*num_nodes]
         
        #  start the processing for the batch ,( total of # iterations)       
        for i in range(num_iterations):

            max_distance = float('-inf')
            
            # start picking up particles, one-by-one
            for particle_index in range(len(particle_position)):
                max_distance = float('-inf')
                current_position = particle_position[particle_index]
                current_velocity = particle_velocity[particle_index]
				# for each particle, go over all the nodes in the current batch 
                for node in node_batch:
                    # check for end of file
                    if node[0] > 26 or node[0] < 0:
                        break
                    # skip nodes that are NOT jammed
                    if node[1] != 1:                   
                        continue
                    else:
                        jam_count=True
                    # store the nodeID 
                    node_id = node[0]
                    # link the current node being processed with it's coordinates ( x,y in another excel file )
                    node_coords = node_coordinates[np.where(node_coordinates[:, 0] == node_id)][0, 1:]
                    x_distance = current_position[0] - node_coords[0]
                    y_distance = current_position[1] - node_coords[1]
                    # euclidean distance between particle and node
                    distance = math.sqrt(x_distance**2 + y_distance**2)
					# minimal covering circle, eg the fitness function is the biggest distance ( furthest node)
                    if distance > max_distance:
                        max_distance = distance
                        particle_current_fitness[particle_index]=max_distance
                # do the necessary checks for personal and global optimum.
                # minimization problem , as we need the smallest circle possible, therefore smallest value wins
                # update when necessary                                                  
                if particle_current_fitness[particle_index]<particle_personal_best_fitness[particle_index]:
                    particle_previous_fitness[[particle_index]]=particle_personal_best_fitness[particle_index]
                    particle_personal_best_fitness[particle_index]=particle_current_fitness[particle_index]
                    particle_personal_best_position[particle_index]=particle_position[particle_index]
                if particle_personal_best_fitness[particle_index]<global_best_fitness and particle_personal_best_fitness[particle_index]!=0.0:
                    global_best_fitness=particle_personal_best_fitness[particle_index]
                    global_best_position[0][0] = particle_position[particle_index][0]
                    global_best_position[0][1] = particle_position[particle_index][1]
                # update particle velocity and position after iterating over all nodes in the batch

                particle_velocity[particle_index] = update_velocity(particle_index, particle_position, particle_velocity, w, c1, c2, particle_personal_best_position, global_best_position)    
                particle_position[particle_index] = update_position(particle_index, particle_position, particle_velocity)
        # also add the error to the sum so that avg error can be calculated 
        # avg error is important, as it tells us how good the algorithm is on the specific scenartio ( jammer location )        
        
        # print("batch : ", node_batch_index+1, "has calculated that the position is : ",  (global_best_position)) 
        error=math.sqrt((jammer_x - global_best_position[0][0])**2 + (jammer_y - global_best_position[0][1])**2)
        # mse = ((jammer_x - global_best_position[0][0])**2 + (jammer_y - global_best_position[0][1])**2)/2
        # rmse = math.sqrt(((jammer_x - global_best_position[0][0])**2 + (jammer_y - global_best_position[0][1])**2)/2)
        if(jam_count):
            print("batch : ", node_batch_index+1, " euclidean distance error :  ", error)
            # print(error)

        else:
            print("batch : ", node_batch_index+1, " SKIPPED ")    
   
        
        



                   
    return 1

# function for the update of a particle's velocity. 
def update_velocity(particle_index, particle_position, particle_velocity, w, c1, c2, personal_best, global_best):
    r1 = random.uniform(0, 1)
    r2 = random.uniform(0, 1)

    velocity = particle_velocity[particle_index]
    velocity[0] = w * velocity[0] + c1 * r1 * (personal_best[particle_index][0] - particle_position[particle_index][0]) + c2 * r2 * (global_best[0][0] - particle_position[particle_index][0])
    velocity[1] = w * velocity[1] + c1 * r1 * (personal_best[particle_index][1] - particle_position[particle_index][1]) + c2 * r2 * (global_best[0][1] - particle_position[particle_index][1])
    return velocity
  
# function for updating a particle's postion   
def update_position(particle_index, particle_position, particle_velocity):
    x = particle_position[particle_index, 0] + particle_velocity[particle_index, 0]
    y = particle_position[particle_index, 1] + particle_velocity[particle_index, 1]
    return np.array([x, y])
    # return particle_position


# calculate average error , while skipping first batch 
average_error=(calculate_fitness(jammed_info,node_coordinates,w,c1,c2))/14

pet = time.process_time()

pres = pet - pst
print('CPU Execution time:', pres, 'seconds')

