import numpy as np 
import math 
np.set_printoptions(precision = 4, suppress=True)


def ADI(tempLeft=75,tempRight=50,tempTop=100,tempBottom=0,tempPlate=0,delta=10,x_node=3,y_node=3,finalTime=30,timeStep=10,k=0.835):
    lamb = k*timeStep/delta**2
    temperPlate = np.full([y_node+2,x_node+2],tempPlate,dtype=float)

    for i in range(len(temperPlate)-1):
        temperPlate[0] = tempBottom
        temperPlate[len(temperPlate)-1] = tempTop
        if 0 < i < len(temperPlate)-1:
            temperPlate[i][0] = tempLeft
            temperPlate[i][len(temperPlate[0])-1] = tempRight
    # print(temperPlate)

    matrixLargeLeftY = np.zeros([y_node,y_node],dtype = float)
    matrixLargeRightY = np.zeros([y_node,y_node],dtype = float)
    matrixLargeLeftX = np.zeros([x_node,x_node],dtype = float)
    matrixLargeRightX = np.zeros([x_node,x_node],dtype = float)
    # print(matrixLargeLeft)
    # print(matrixLargeRight)

    #start of making static arrays
    #When moving in the Y direction
    for i in range(y_node):
        #first row
        if i == 0:
            matrixLargeLeftY[i,i]=2*(1+(lamb))
            matrixLargeLeftY[i,i+1]=-1*lamb
        elif i == y_node-1:
            matrixLargeLeftY[i,i-1]=-1*lamb
            matrixLargeLeftY[i,i]=2*(1+(lamb))
        #second row
        else:
            matrixLargeLeftY[i,i-1]=-1*lamb
            matrixLargeLeftY[i,i]=2*(1+(lamb))
            matrixLargeLeftY[i,i+1]=-1*lamb
    # print('matrix left\n',matrixLargeLeftY)

    for i in range(y_node):
        #large right matrix
        matrixLargeRightY[i,i] = (2*(1-(lamb)))
        if i+3 < y_node:
            matrixLargeRightY[i,i+3] = lamb
            matrixLargeRightY[i+3,i] = lamb
    # print('matrix right\n',matrixLargeRightY)

    #when moving in the X direction
    for i in range(x_node):
        #first row
        if i == 0:
            matrixLargeLeftX[i,i]=2*(1+(lamb))
            matrixLargeLeftX[i,i+1]=-1*lamb
        elif i == x_node-1:
            matrixLargeLeftX[i,i-1]=-1*lamb
            matrixLargeLeftX[i,i]=2*(1+(lamb))
        #second row
        else:
            matrixLargeLeftX[i,i-1]=-1*lamb
            matrixLargeLeftX[i,i]=2*(1+(lamb))
            matrixLargeLeftX[i,i+1]=-1*lamb
    # print('matrix left\n',matrixLargeLeftX)

    for i in range(x_node):
        #large right matrix
        matrixLargeRightX[i,i] = (2*(1-(lamb)))
        if i+3 < x_node:
            matrixLargeRightX[i,i+3] = lamb
            matrixLargeRightX[i+3,i] = lamb
    # print('matrix right\n',matrixLargeRightX)

    timer = 0
    while(timer<=300):
    #     # print(timer)
        #half time step in the Y direction
        for i in range(1,x_node+1):
            boundaryStorage = []
            holderPlatetemps = []
            for j in range(1,y_node+1):
                if i == 1 and j == 1:
                    boundaryStorage.append(temperPlate[j,i-1]+temperPlate[j-1,i]+temperPlate[j,i+1]+temperPlate[j,i])
                if i == 1 and j == y_node:
                    boundaryStorage.append(temperPlate[j,i-1]+temperPlate[j+1,i]+temperPlate[j,i+1]+temperPlate[j,i])
                if i == x_node and j == 1:
                    boundaryStorage.append(temperPlate[j,i+1]+temperPlate[j-1,i]+temperPlate[j,i-1]+temperPlate[j,i])
                if i ==x_node and j == y_node:
                    boundaryStorage.append(temperPlate[j,i+1]+temperPlate[j+1,i]+temperPlate[j,i-1]+temperPlate[j,i])
                if (i == 1 or i == x_node) and 1 < j < y_node:
                    boundaryStorage.append(temperPlate[j,i+1]+temperPlate[j,i-1]+temperPlate[j,i])
                if (j==1 or j == y_node) and 1 < i < x_node:
                    if j == 1:
                        boundaryStorage.append(temperPlate[j-1,i]+temperPlate[j,i+1]+temperPlate[j,i-1])
                    else:
                        boundaryStorage.append(temperPlate[j+1,i]+temperPlate[j,i+1]+temperPlate[j,i-1])
                if (i > 1 and j > 1) and (i < x_node and j < y_node):
                    boundaryStorage.append(temperPlate[j,i+1]+temperPlate[j,i-1])
                holderPlatetemps.append(temperPlate[j,i])

            boundStorage = np.reshape(boundaryStorage,(-1,1))
            # print(boundStorage)
            holderPlatetemps = np.reshape(holderPlatetemps,(-1,1))
            # print(holderPlatetemps)
            combinedLambAndBound = lamb*boundStorage
            # print(combinedLambAndBound)
            combinedPlateAndMLR = np.dot(matrixLargeRightY,holderPlatetemps)
            # print(combinedPlateAndMLR)
            combinedRight = combinedLambAndBound+combinedPlateAndMLR
            # print(combinedRight)
            newPlateTemps = np.linalg.solve(matrixLargeLeftY,combinedRight)
            # print(newPlateTemps)
            for j in range(len(newPlateTemps)):
                temperPlate[j+1,i] = newPlateTemps[j,0]
        # print(temperPlate)

        for j in range(1,y_node+1):
            boundaryStorage = []
            holderPlatetemps = []
            for i in range(1,x_node+1):
                if i == 1 and j == 1:
                    # boundaryStorage.append(temperPlate[j+1,i]+temperPlate[j-1,i]+temperPlate[j,i-1])
                    boundaryStorage.append(temperPlate[j+1,i]+temperPlate[j-1,i]+temperPlate[j,i-1]+temperPlate[j,i])
                if i == 1 and j == y_node:
                    boundaryStorage.append(temperPlate[j,i-1]+temperPlate[j+1,i]+temperPlate[j-1,i]+temperPlate[j,i])
                if i == x_node and j == 1:
                    boundaryStorage.append(temperPlate[j,i+1]+temperPlate[j-1,i]+temperPlate[j+1,i]+temperPlate[j,i])
                if i ==x_node and j == y_node:
                    boundaryStorage.append(temperPlate[j,i+1]+temperPlate[j+1,i]+temperPlate[j-1,i]+temperPlate[j,i])
                if (j == 1 or j == y_node) and 1 < i < x_node:
                    boundaryStorage.append(temperPlate[j+1,i]+temperPlate[j-1,i]+temperPlate[j,i])
                if (i==1 or i == x_node) and 1 < j < y_node:
                    if i == 1:
                        boundaryStorage.append(temperPlate[j-1,i]+temperPlate[j,i-1]+temperPlate[j+1,i]+temperPlate[j,i])
                    else:
                        boundaryStorage.append(temperPlate[j+1,i]+temperPlate[j,i+1]+temperPlate[j-1,i]+temperPlate[j,i])
                if (i > 1 and j > 1) and (i < x_node and j < y_node):
                    boundaryStorage.append(temperPlate[j+1,i]+temperPlate[j-1,i]+temperPlate[j,i])
                holderPlatetemps.append(temperPlate[j,i])

            boundaryStorage = np.reshape(boundaryStorage,(-1,1))
            # print(boundaryStorage)
            holderPlatetemps = np.reshape(holderPlatetemps,(-1,1))
            combinedLambAndBound = lamb*boundStorage
            # print(combinedLambAndBound)
            combinedPlateAndMLR = np.dot(matrixLargeRightX,holderPlatetemps)
            # print(combinedPlateAndMLR)
            combinedRight = combinedLambAndBound+combinedPlateAndMLR
            # print('combined',combinedRight)
            newPlateTemps = np.linalg.solve(matrixLargeLeftX,combinedRight)
            for i in range(len(newPlateTemps)):
                temperPlate[j,i+1] = newPlateTemps[i,0]
        
    #     # print(temperPlate)
        timer += timeStep
        if timer%100 == 0:
            print(temperPlate)
ADI()
# ADI(delta=5,x_node=6,y_node=4)