import numpy as np 
import math 
np.set_printoptions(precision = 4, suppress=True)

def corner(lamb,left,selfn,right,other):
    return lamb*left+(2*(1-lamb))*selfn+lamb*right+lamb*other

def sideNside(lamb,side1,selfn,side2):
    return lamb*side1+(2*(1-lamb))*selfn+lamb*side2

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
    matrixLargeLeftX = np.zeros([x_node,x_node],dtype = float)
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
    
    timer = 0
    while(timer<300):
        for i in range(1,x_node+1):
            boundaryStorage=[]
            for j in range(1,y_node+1):
                if (i == 1 or i == x_node) and j == 1:
                    boundaryStorage.append(corner(lamb,temperPlate[j,i-1],temperPlate[j,i],temperPlate[j,i+1],temperPlate[j-1,i]))
                elif (i == 1 or i == x_node) and j == y_node:
                    boundaryStorage.append(corner(lamb,temperPlate[j,i-1],temperPlate[j,i],temperPlate[j,i+1],temperPlate[j+1,i]))
                elif (1<i<x_node) and j == 1:
                    boundaryStorage.append(corner(lamb,temperPlate[j,i-1],temperPlate[j,i],temperPlate[j,i+1],temperPlate[j-1,i]))
                elif (1<i<x_node) and j == y_node:
                    boundaryStorage.append(corner(lamb,temperPlate[j,i-1],temperPlate[j,i],temperPlate[j,i+1],temperPlate[j+1,i]))
                else:
                    boundaryStorage.append(sideNside(lamb,temperPlate[j,i-1],temperPlate[j,i],temperPlate[j,i+1]))
            boundaryStorage = np.reshape(boundaryStorage,(-1,1))
            # print(boundaryStorage)
            newPlateTemps = np.linalg.solve(matrixLargeLeftY,boundaryStorage)
            # print(newPlateTemps)
            for j in range(len(newPlateTemps)):
                    temperPlate[j+1,i] = newPlateTemps[j,0]
            # print(temperPlate)
        # print(temperPlate)
        for j in range(1,y_node+1):
            boundaryStorage=[]
            for i in range(1,x_node+1):
                if (j == 1 or j == y_node) and i == 1:
                    boundaryStorage.append(corner(lamb,temperPlate[j-1,i],temperPlate[j,i],temperPlate[j+1,i],temperPlate[j,i-1]))
                elif (j == 1 or j == y_node) and i == x_node:
                    boundaryStorage.append(corner(lamb,temperPlate[j-1,i],temperPlate[j,i],temperPlate[j+1,i],temperPlate[j,i+1]))
                elif (1<j<y_node) and i == 1:
                    boundaryStorage.append(corner(lamb,temperPlate[j-1,i],temperPlate[j,i],temperPlate[j+1,i],temperPlate[j,i-1]))
                elif (1<j<y_node) and i == x_node:
                    boundaryStorage.append(corner(lamb,temperPlate[j-1,i],temperPlate[j,i],temperPlate[j+1,i],temperPlate[j,i+1]))
                else:
                    boundaryStorage.append(sideNside(lamb,temperPlate[j-1,i],temperPlate[j,i],temperPlate[j+1,i]))
            boundaryStorage = np.reshape(boundaryStorage,(-1,1))
            # print(boundaryStorage)
            newPlateTemps = np.linalg.solve(matrixLargeLeftX,boundaryStorage)
            # print(newPlateTemps)
            for i in range(len(newPlateTemps)):
                    temperPlate[j,i+1] = newPlateTemps[i,0]
        timer += timeStep
        if timer%100 == 0:
            print(temperPlate) 

    returntemp = np.delete(temperPlate,0,0)
    returntemp = np.delete(returntemp,0,1)
    returntemp = np.delete(returntemp,len(returntemp)-1,0)
    returntemp = np.delete(returntemp,len(returntemp[0])-1,1)
    return returntemp   

ADI()
# ADI(delta=5,x_node=6,y_node=4)