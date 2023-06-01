

import sys 
import math
import time
import pandas as pd
pst = time.process_time()


df = pd.read_excel("./Reactive_random/reactive_random_ALL_values.xlsx", sheet_name="fuzzy_(4)")
jammer_x=60.00
jammer_y=-20.00
array = df.values.tolist()
    
  
nodes_df = pd.read_excel("./Constant_random/random_thesi.xlsx",sheet_name="Sheet1", header=None)
node_batch_index=1
node_coordinates = nodes_df.values.tolist() 

length= len(array)
start_time = time.time()
count = 0 #counter to find how many 1 we have 
weights=0
arrayForX = 0
jam_count=0
arrayForY=0
sumX = 0
sumY=0
for i,j  in zip(array,node_coordinates):
        
    if((i[7])!=1.0 and (i[7]!=0.0)):
        continue
    count = count +1
    if float(i[6]) > 0.575 :
        jam_count = jam_count + 1    
        weights = weights +float(i[6])
        arrayForX= (i[6]) * (j[0])
        sumX = sumX + arrayForX
        arrayForY= (i[6]) *(j[1])
        sumY = sumY + arrayForY
    if count == 24:  # Once 24 nodes have been processed, calculate the centroid
        if (jam_count==0):
            print("SKIPPED BATCH : ", node_batch_index )
            count = 0
            arrayForX = 0
            sumX = 0
            arrayForY = 0
            sumY = 0
            jam_count=0
            weights=0
            node_batch_index +=1
            continue;
        
        Xestimate = sumX / weights
        Yestimate = sumY / weights
        error=math.sqrt((jammer_x - Xestimate)**2 + (jammer_y - Yestimate)**2)
        mse = ((jammer_x - Xestimate)**2 + (jammer_y - Yestimate)**2)/2
        rmse = math.sqrt(((jammer_x - Xestimate)**2 + (jammer_y - Yestimate)**2)/2)
        count = 0
        arrayForX = 0
        sumX = 0
        arrayForY = 0
        sumY = 0
        jam_count=0
        weights=0
        # print("batch : ", node_batch_index, " has calculated :  ", Xestimate , " ", Yestimate) 
        # print("batch : ", node_batch_index, " euclidean distance error :  ", error)
        print(error) 

        # print("batch : ", node_batch_index, " mse distance error :  ", mse) 
        # print("batch : ", node_batch_index, " rmse distance error :  ", rmse) 
        error=0
        node_batch_index +=1

pet = time.process_time()


pres = pet - pst

print('CPU Execution time:', pres, 'seconds')