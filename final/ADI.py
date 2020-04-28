import numpy as np 
import math 
import json 
np.set_printoptions(precision = 4, suppress=True)

def ADI(tempLeft=75,tempRight=50,tempTop=100,tempBottom=0,tempPlate=0,delta=5,x_node=6,y_node=4,finalTime=300,timeStep=10,k=0.835):
    # new_x = int((x_node)/delta)+1
    # new_y = int((y_node)/delta)+1
    new_x = x_node
    new_y = y_node
    # print(new_x,new_y)
    lamb = k*timeStep/delta**2
    temperatureBlock = np.full(shape=[new_y,new_x],fill_value=tempPlate,dtype=float)
    staticMatrixLen = (len(temperatureBlock)-2)**2
    
    # plate = np.full(shape=new_x,fill_value=tempPlate)
    for i in range(new_y-1):
        temperatureBlock[0] = tempBottom
        temperatureBlock[new_y-1] = tempTop
        if 0 < i < new_y-1:
            temperatureBlock[i][0] = tempLeft
            temperatureBlock[i][new_x-1] = tempRight

    holderArray = np.copy(temperatureBlock)
    matrixLargeLeft = np.zeros([staticMatrixLen,staticMatrixLen],dtype = float)
    matrixLargeRight = np.zeros([staticMatrixLen,staticMatrixLen],dtype = float)

    #start of making static arrays
    for i in range(0,staticMatrixLen-1,3):
        #first row
        matrixLargeLeft[i,i]=2*(1+(lamb))
        matrixLargeLeft[i,i+1]=-1*lamb
        #second row
        matrixLargeLeft[i+1,i]=-1*lamb
        matrixLargeLeft[i+1,i+1]=2*(1+(lamb))
        matrixLargeLeft[i+1,i+2]=-1*lamb
        #third row
        matrixLargeLeft[i+2,i+1]=-1*lamb
        matrixLargeLeft[i+2,i+2]=2*(1+(lamb))
    # print('matrix left\n',matrixLargeLeft)
    
    for i in range(staticMatrixLen):
        #large right matrix
        matrixLargeRight[i,i] = (2*(1-(lamb)))
        if i+3 < staticMatrixLen:
            matrixLargeRight[i,i+3] = lamb
            matrixLargeRight[i+3,i] = lamb
    # print('matrix right\n',matrixLargeRight)
    
    boundaryStorageStepHalf = []
    for i in range(1,new_x-1):
        for j in range(1,new_y-1):
            if i == 1 and j == 1:
                boundaryStorageStepHalf.append(temperatureBlock[j,i-1]+temperatureBlock[i-1,i])
            if i == 1 and j == new_y-2:
                boundaryStorageStepHalf.append(temperatureBlock[j,i-1]+temperatureBlock[j+1,i])
            if i == new_x-2 and j == 1:
                boundaryStorageStepHalf.append(temperatureBlock[j,i+1]+temperatureBlock[j-1,i])
            if i ==new_x-2 and j == new_y-2:
                boundaryStorageStepHalf.append(temperatureBlock[j,i+1]+temperatureBlock[j+1,i])
            if (i == 1 or i == new_x-2) and 1 < j < new_y-2:
                if i ==1:
                    boundaryStorageStepHalf.append(temperatureBlock[j,i-1])
                else:
                    boundaryStorageStepHalf.append(temperatureBlock[j,i+1])
            if (j==1 or j == new_y-2) and 1 < i < new_x-2:
                if j ==1:
                    boundaryStorageStepHalf.append(temperatureBlock[j-1,i])
                else:
                    boundaryStorageStepHalf.append(temperatureBlock[j+1,i])
            if (i > 1 and j > 1) and (i < new_x-2 and j < new_y-2):
                boundaryStorageStepHalf.append(0)
    boundaryStorageStepHalf = np.reshape(boundaryStorageStepHalf,(-1,1))
    # print(boundaryStorageStepHalf)
    boundaryStorageStepHalf = lamb*boundaryStorageStepHalf
    # print(boundaryStorageStepHalf)

    boundaryStorageFullStep = []
    for j in range(1,new_y-1):
        for i in range(1,new_x-1):
            if i == 1 and j == 1:
                boundaryStorageFullStep.append(temperatureBlock[j,i-1]+temperatureBlock[i-1,i])
            if i == 1 and j == new_y-2:
                boundaryStorageFullStep.append(temperatureBlock[j,i-1]+temperatureBlock[j+1,i])
            if i == new_x-2 and j == 1:
                boundaryStorageFullStep.append(temperatureBlock[j,i+1]+temperatureBlock[j-1,i])
            if i ==new_x-2 and j == new_y-2:
                boundaryStorageFullStep.append(temperatureBlock[j,i+1]+temperatureBlock[j+1,i])
            if (i == 1 or i == new_x-2) and 1 < j < new_y-2:
                if i ==1:
                    boundaryStorageFullStep.append(temperatureBlock[j,i-1])
                else:
                    boundaryStorageFullStep.append(temperatureBlock[j,i+1])
            if (j==1 or j == new_y-2) and 1 < i < new_x-2:
                if j ==1:
                    boundaryStorageFullStep.append(temperatureBlock[j-1,i])
                else:
                    boundaryStorageFullStep.append(temperatureBlock[j+1,i])
            if (i > 1 and j > 1) and (i < new_x-2 and j < new_y-2):
                boundaryStorageFullStep.append(0)
    boundaryStorageFullStep = np.reshape(boundaryStorageFullStep,(-1,1))
    # print(boundaryStorageFullStep)
    boundaryStorageFullStep = lamb*boundaryStorageFullStep
    # print(boundaryStorageFullStep)
    #end of making static arrays
    
    timer = 0
    while(timer<=finalTime*timeStep):
        #half step
        tempStorage = []
        for i in range(1,new_y-1):
            for j in range(1,new_x-1):
                tempStorage.append(temperatureBlock[j,i])
        tempStorage = np.reshape(tempStorage,(-1,1))
        # print(tempStorage)

        #doing all the math, first gets the dot product of the plate temperatures
        #and the static right large matrix, then adds the two matrix on the right side of the equation to 
        #make the "C" matrix for linear solve, reshapes it to a 3x3 to then plug back into the holder array.
        dotArray = np.dot(matrixLargeRight,tempStorage)
        # print('dot matrix\n',dotArray)
        combinedMatrixRight = dotArray+boundaryStorageStepHalf
        # print('combined matrix right\n',combinedMatrixRight)
        newPlateTemps = np.linalg.solve(matrixLargeLeft,combinedMatrixRight)
        # print('new plate temps\n',newPlateTemps)
        newPlateTemps = np.reshape(newPlateTemps,[int(math.sqrt(staticMatrixLen)),int(math.sqrt(staticMatrixLen))])
        newPlateTemps = np.transpose(newPlateTemps)
        for i in range(int(math.sqrt(staticMatrixLen))):
            for j in range(int(math.sqrt(staticMatrixLen))):
                holderArray[j+1,i+1] = newPlateTemps[j,i]
        temperatureBlock = np.copy(holderArray)
        # print(temperatureBlock)
        # print(temperatureBlock[1,2])


        #full step
        #creates an array to store the plates temperatures then converts from a 3x3 to a 1x9
        tempStorage = []
        for j in range(1,new_x-1):
            for i in range(1,new_y-1):
                tempStorage.append(temperatureBlock[j,i])
        tempStorage = np.reshape(tempStorage,(-1,1))

        #doing all the math, first gets the dot product of the plate temperatures
        #and the static right large matrix, then adds the two matrix on the right side of the equation to 
        #make the "C" matrix for linear solve, reshapes it to a 3x3 to then plug back into the block.
        dotArray = np.dot(matrixLargeRight,tempStorage)
        combinedMatrixRight = dotArray+boundaryStorageFullStep
        newPlateTemps = np.linalg.solve(matrixLargeLeft,combinedMatrixRight)
        # print('new plate temps\n',newPlateTemps)
        newPlateTemps = np.reshape(newPlateTemps,[int(math.sqrt(staticMatrixLen)),int(math.sqrt(staticMatrixLen))])
        # newPlateTemps = np.transpose(newPlateTemps)
        for i in range(int(math.sqrt(staticMatrixLen))):
            for j in range(int(math.sqrt(staticMatrixLen))):
                temperatureBlock[j+1,i+1] = newPlateTemps[j,i]
        # print(temperatureBlock)

        #increiments the timer
        timer+=timeStep
        # print(timer)
        #prints for every 100s
        if timer%100 == 0:
            print(temperatureBlock)
    returntemp = np.delete(temperatureBlock,0,0)
    returntemp = np.delete(returntemp,0,1)
    returntemp = np.delete(returntemp,len(returntemp)-1,0)
    returntemp = np.delete(returntemp,len(returntemp[0])-1,1)
    return temperatureBlock

if __name__ == "__main__":
    pass
ADI()    
# ADI(k=10**-4,tempLeft=100,tempRight=100,tempTop=100,tempBottom=100,tempPlate=200,x_node=1,y_node=1,delta=.25,finalTime=1000,timeStep=100)