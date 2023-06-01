# double cicles algorithm

# input positions of jammed nodes and boundary nodes
# jammed nodes are the ones that have 1 in dataset.
# A node is considered to be a boundary node if it lost
# some of neighbors while it can communicate with part of unaffected nodes.
# output: estimated position

import math
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull, convex_hull_plot_2d, distance
from helper import Point, welzl
# import distance as d
import time
import gc

pst = time.process_time()

def calc_minimum_bounding_circles(boundaryhpoints, jammedhpoints):
    bhpoints = []
    for points in boundaryhpoints:
        bhpoints.append(Point(points[0], points[1]))

    jhpoints = []
    for points in jammedhpoints:
        jhpoints.append(Point(points[0], points[1]))

    # calculate circles of each

    mbc_bounding = welzl(bhpoints)
    mbc_jammed = welzl(jhpoints)


    return (mbc_bounding, mbc_jammed)




def calculate_jammer_position(filename, debug):
    start = time.time()
    data = pd.read_excel(filename,sheet_name="fuzzy_(4)")
    data.iloc[1]
    
    actualx = data['actual_X'].iloc[0]
    actualy = data['actual_y'].iloc[0]

    # get the number of nodes per batch
    nodes_per_batch = 24

    # get the total number of batches
    num_batches = 14
    # process each batch individually
    for batch_num in range(num_batches):
        boundary = None
        jammed = None
        boundary_hull = None
        jammed_hull = None
        mbc_bounding = None
        mbc_jammed = None
        # get the start and end indices of the current batch
        start_index = batch_num * nodes_per_batch
        end_index = (batch_num + 1) * nodes_per_batch

        # get the data for the current batch
        batch_data = data.iloc[start_index:end_index]
        


        # fuzzy column is un needed
        batch_data = batch_data.copy() # make a copy of the DataFrame slice

        batch_data.drop(columns=['Fuzzy'], inplace=True)

        # drop the unneeded columns
        batch_data.drop(columns=['actual_X'], inplace=True)
        batch_data.drop(columns=['actual_y'], inplace=True)

        

        # get unbounded nodes, the ones that have 0 in affected
        boundary = batch_data.drop(batch_data[(batch_data['affected'] == 1)].index, axis=0)

        # remove affected column
        boundary.drop(columns=['affected'], inplace=True)

        # reset dataframe index
        boundary.reset_index(drop=True, inplace=True)
        boundary = boundary.to_numpy()

        # get jammed nodes, the ones that have 1 in affected
        jammed = batch_data.drop(batch_data[(batch_data['affected'] == 0)].index, axis=0)

        # remove affected column
        jammed.drop(columns=['affected'], inplace=True)

        # reset dataframe index
        jammed.reset_index(drop=True, inplace=True)
        # convert to numpy array

        jammed = jammed.to_numpy()

        # calculate 2 convex hulls
        # one with the jammed nodes
        # one with the boundary nodes


        if ( len(boundary)<= 0 or len(jammed)<=0):
                    # reset relevant variables for the next batch
            print("SKIPPED BATCH : ", batch_num+1)        
            del boundary, jammed, boundary_hull, jammed_hull, mbc_bounding, mbc_jammed
            gc.collect()
            continue;
          
    # Check if there are enough boundary and jammed nodes
        if len(boundary) < 3 or len(jammed) < 3:
            print("SKIPPED BATCH : ", batch_num+1 , " NOT ENOUGH NODES TO MAKE A HULL")        
            del boundary, jammed, boundary_hull, jammed_hull, mbc_bounding, mbc_jammed
            gc.collect()
            continue;   
                       
        if len(boundary) > 0:
            boundary_hull = ConvexHull(boundary)  
        if len(jammed) > 0:
            jammed_hull = ConvexHull(jammed)





        if debug:
            print('Points:\n', boundary_hull.points)
            if (len (jammed>0)):
                print('Points:\n', jammed_hull.points)

        # calculate the minimum bounding circles
        
        
        
        
        
        mbc_bounding, mbc_jammed = calc_minimum_bounding_circles(
            boundary_hull.points, jammed_hull.points)

        # calculate the positon of the jammer
        x = (mbc_jammed.C.X-mbc_bounding.C.X)
        y = (mbc_jammed.C.Y-mbc_bounding.C.Y)
        # print(f'Batch {batch_num+1} - Predicted position: ', x, y)

        distance_error = math.sqrt((actualx-x)**2+(actualy-y)**2)
        print(f'Batch {batch_num+1} - Distance error: ', distance_error)
        # print(distance_error)

        # reset relevant variables for the next batch
        del boundary, jammed, boundary_hull, jammed_hull, mbc_bounding, mbc_jammed
        gc.collect()

    stop = time.time()
    time_taken = stop-start
    
    
    
    
    
    
    
    return distance_error,time_taken


def main():
            error=0
            timeF=0
            filename = 'concat_values.csv'
            error, timeF = calculate_jammer_position('./Reactive_random/reactive_random_concat_values.xlsx', False)
            pet = time.process_time()


            pres = pet - pst

            print('CPU Execution time:', pres, 'seconds')



if __name__ == '__main__':
    main()
