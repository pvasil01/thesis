import sys
import time

import numpy as np
import math
import pandas as pd
pst = time.process_time()


def distance(x1, y1, x2, y2):
    one = (x1 - x2) ** 2
    two = (y1 - y2) ** 2
    return math.sqrt(one + two)

def main():
    start_time = time.time()

    df = pd.read_excel("./Reactive_random/reactive_random_ALL_values.xlsx", sheet_name="fuzzy_(8)")
    jammer_x=60.00
    jammer_y=-20.00
    array = df.values.tolist()
        
    
    nodes_df = pd.read_excel("./Constant_random/random_thesi.xlsx",sheet_name="Sheet1", header=None)

    node_batch=0
    coordinate_batch=0
            
  
    node_batch_index=0
    coordinate_batch_index=0
    node_coordinates = nodes_df.values.tolist() 

    length = len(array)
    start_time = time.time()
    count = 0  # counter to find how many 1 we have
    jam_count=0
    coordinate_batches = [node_coordinates[i:i+24] for i in range(0, len(node_coordinates), 24)]
    node_batches = [array[i:i+24] for i in range(0, len(array), 24)]

    for node_batch, coordinate_batch in zip (node_batches,coordinate_batches):
        Max = []
        maxX = []
        maxY = []
        sumX=0
        sumY=0
        arrayForX=0
        arrayForY=0
        count=0
        jam_count=0
        Xestimate=0
        Yestimate=0
        Xestimate2=0
        Yestimate2=0
        max_d = 0
        max_x = 0
        max_y=0
        temp=0
        F_Pull = []
        F_Push = []
        pullX=0
        pullY=0
        pushX=0
        pushY=0
        sum_sqX =0
        rootX = 0
        sum_sqY =0
        rootY =0
        DistanceJamRange = 0
        sum_x_pull = 0
        sum_y_pull = 0
        sum_x_push = 0
        sum_y_push = 0
        SumJoint=0



        for i, j in zip(node_batch,coordinate_batch):
    
                if(int(i[7])!=1.0 and int(i[7]!=0.0)):
                        continue
                count=count+1    
                if int(i[7]) == 1.0:
                    jam_count = jam_count + 1
                    
                        
                arrayForX = (i[7]) * (j[0])
                arrayForY = (i[7]) * (j[1])
                sumX = sumX + arrayForX
                sumY = sumY + arrayForY         

                
        if (jam_count==0):
            print ( "node_batch ID : ", node_batch_index +1, "SKIPPED")            
            count = 0
            arrayForX = 0
            sumX = 0
            arrayForY = 0
            sumY = 0
            jam_count=0
            node_batch_index+=1
            coordinate_batch_index+=1
            
            continue;
        Xestimate = float(sumX / jam_count)


        Yestimate = float(sumY / jam_count)






        for i,j in zip(node_batch,coordinate_batch):

                if int(i[7]) == 1.0:
                    temp = distance(Xestimate, Yestimate, float(j[0]), float(j[1]))
                    if temp > max_d:
                        max_d = temp
                        max_x = j[0]
                        max_y=j[1]

        maxX = float(max_x)
        maxY = float(max_y)

            # Estimated area

        Xestimate2 = float(Xestimate)
        Yestimate2 = float(Yestimate)
            # Pull, Push Formula
        sumPullX = 0
        sumPullY = 0
        sumPushX = 0
        sumPushY = 0

        for i, j in zip(node_batch,coordinate_batch):

                if float(j[0]) == Xestimate2 and float(j[1]) == Yestimate2:
                    pass
                else:
                    if int(i[7]) == 1.0:

                        pullX = (float(j[0]) - Xestimate2) / math.sqrt(
                            math.pow(float(j[0]) - Xestimate2, 2) + math.pow(float(j[1]) - Yestimate2, 2))
                        pullY = (float(j[1]) - Yestimate2) / math.sqrt(
                            math.pow(float(j[0]) - Xestimate2, 2) + math.pow(float(j[1]) - Yestimate2, 2))

                        F_Pull.append({'x': pullX, 'y': pullY})

                    else:

                        pushX = (Xestimate2 - float(j[0])) / math.sqrt(
                            math.pow(Xestimate2 - float(j[0]), 2) + math.pow(Yestimate2 - float(j[1]), 2))
                        pushY = (Yestimate2 - float(j[1])) / math.sqrt(
                            math.pow(Xestimate2 - float(j[0]), 2) + math.pow(Yestimate2 - float(j[1]), 2))

                        F_Push.append({'x': pushX, 'y': pushY})

        sum_sqX = np.sum(np.square(pushX - pullX))
        rootX = np.sqrt(sum_sqX)

        sum_sqY = np.sum(np.square(pushY - pullY))
        rootY = np.sqrt(sum_sqY)
        

        DistanceJamRange = rootX + rootY

            
           
            # Joint Formula
        for index, z in enumerate(F_Push):

                sum_x_push = sum_x_push + z['x']
                sum_y_push = sum_y_push + z['y']

        for index, z in enumerate(F_Pull):

                sum_x_pull = sum_x_pull + z['x']
                sum_y_pull = sum_y_pull + z['y']

        SumJoint = (sum_x_push + sum_x_pull) / abs(sum_y_push + sum_y_pull)
        SumJoint = (sum_x_push + sum_x_pull) / abs(sum_y_push + sum_y_pull)

        Xestimate2 = Xestimate2 + SumJoint * DistanceJamRange
        Yestimate2 = Yestimate2 + SumJoint * DistanceJamRange

        # print("New estimated jammer's position:", Xestimate2, Yestimate2)

        timet=time.time() - start_time

        error=math.sqrt((jammer_x - Xestimate2)**2 + (jammer_y - Yestimate2)**2)
        print("Batch num : ", node_batch_index+1,"The error rate is:", error)
        # print(error)
        
        coordinate_batch_index+=1
        node_batch_index+=1

     
     
     
    pet = time.process_time()


    pres = pet - pst

    print('CPU Execution time:', pres, 'seconds')           


if __name__ == '__main__':
    main()