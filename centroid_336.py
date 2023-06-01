
import sys 
import math
import time
import pandas as pd
pst = time.process_time()


df = pd.read_excel("./Reactive_random/reactive_random_ALL_values.xlsx", sheet_name="fuzzy_(8)")
jammer_x=60.00
jammer_y=-20.00
array = df.values.tolist()
    
  
nodes_df = pd.read_excel("./Constant_random/random_thesi.xlsx",sheet_name="Sheet1", header=None)
node_batch_index=1
node_coordinates = nodes_df.values.tolist() 

length = len(array)
count = 0  # counter to find how many 1 we have



arrayForX = 0
jam_count=0
arrayForY=0
sumX = 0
sumY=0
for i,j  in zip(array,node_coordinates):
    
    if((i[7])!=1.0 and (i[7]!=0.0)):
        continue
    count = count + 1    

    if (i[7]) == 1.0:
        jam_count = jam_count + 1    


    arrayForX = (i[7]) * (j[0])
    arrayForY = (i[7]) * (j[1])
    sumX = sumX + arrayForX
    sumY = sumY + arrayForY    
    if count == 24:  # Once 24 nodes have been processed, calculate the centroid
        if (jam_count==0):
            print ( " BATCH : " , node_batch_index, " skipped ")
            count = 0
            arrayForX = 0
            sumX = 0
            arrayForY = 0
            sumY = 0
            jam_count=0
            node_batch_index +=1
            continue;
        
        Xestimate = sumX / jam_count
        Yestimate = sumY / jam_count
        error=math.sqrt((jammer_x - Xestimate)**2 + (jammer_y - Yestimate)**2)
        mse = ((jammer_x - Xestimate)**2 + (jammer_y - Yestimate)**2)/2
        rmse = math.sqrt(((jammer_x - Xestimate)**2 + (jammer_y - Yestimate)**2)/2)
        count = 0
        arrayForX = 0
        sumX = 0
        arrayForY = 0
        sumY = 0
        jam_count=0
        # print("batch : ", node_batch_index, " has calculated :  ", Xestimate , " ", Yestimate) 
        print("batch : ", node_batch_index, " euclidean distance error :  ", error)
        # print(error) 

        # print("batch : ", node_batch_index, " mse distance error :  ", mse) 
        # print("batch : ", node_batch_index, " rmse distance error :  ", rmse) 
        node_batch_index +=1
        
pet = time.process_time()


pres = pet - pst

print('CPU Execution time:', pres, 'seconds')




