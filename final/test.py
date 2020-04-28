import numpy as np 
import math

neglambAndBeta = np.array([[2.167,-0.083,0],[-0.085,2.167,-0.035],[0,-0.0835,2.167]],dtype=float)
firstbound = np.array([[6.2625],[6.2625],[14.6125]])
secondbound = np.array([[0],[0],[8.35]],dtype=float)
thirdbound = np.array([[4.175],[4.175],[12.525]],dtype=float)
finallist = np.linalg.solve(neglambAndBeta,firstbound)
print(finallist)
secondgo = finallist+secondbound
print(secondgo)
finallist = np.linalg.solve(neglambAndBeta,secondgo)
print(finallist)

booksolutions1 = np.array([[3.01597],[3.2708],[6.8692]],dtype=float)
booksolutions2 = np.array([[0.1274],[0.2900],[4.1291]],dtype=float)
booksolutions3 = np.array([[2.0181],[2.2477],[6.0256]],dtype=float)
# print(np.dot(neglambAndBeta,booksolutions1))
# print(np.dot(neglambAndBeta,booksolutions2))
# print(np.dot(neglambAndBeta,booksolutions3))

newbound1 = np.dot(neglambAndBeta,booksolutions1)/0.0835
newbound2 = np.dot(neglambAndBeta,booksolutions2)/0.0835
newbound3 = np.dot(neglambAndBeta,booksolutions3)/0.0835
# print(newbound1)
print(newbound2)
# print(newbound3)
# temp = np.reshape(neglambAndBeta,(-1,1))
