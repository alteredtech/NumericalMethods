# import math

# def func(x):
#     return math.sin(x)+math.cos(1+x**2)-1

# def false():
#     xl = -2
#     xu = 2
#     for i in range(2):
#         xr = xu-(func(xu)*(xl-xu)/(func(xl)-func(xu)))
#         print('value of xr '+str(xr))
#         temp = func(xr)*func(xl)
#         print('value of temp '+str(temp))
#         if temp < 0:
#             xu = xr
#         elif temp > 0:
#             xl = xr
#         else:
#             break

# def scant():
#     print(math.radians(math.sin(30)))
#     print(math.radians(math.cos(30)))
#     x = [-2,2]
#     for i in range(1,6):
#         x.append(x[i]-(func(x[i])*(x[i-1]-x[i])/(func(x[i-1])-func(x[i]))))
#         print(x[i])

# scant()

import numpy as np 
import math
import random
np.set_printoptions(precision = 4, suppress=True)

def diff(list1,list2):
        return(list(set(list1)-set(list2)))

if __name__ == "__main__":

    # n = 7
    # l1 = [random.random() for i in range(n)]
    # l1_2 = [random.random()+1 for i in range(n)]
    # l2 = [random.random()*3 for i in range(n)]
    # l3 = [random.random()+5*4 for i in range(n)]
    # print(l1,l1_2,l2,l3)

    # uwl1 = np.unwrap(l1,discont=math.pi,axis=0)
    # uwl1_2 = np.unwrap(l1_2,discont=math.pi,axis=0)
    # uwl2 = np.unwrap(l2,discont=math.pi,axis=0)
    # uwl3 = np.unwrap(l3,discont=math.pi)
    # print('\n\n\n\n\n')
    # print(uwl1,uwl1_2,uwl2,uwl3)

    l1 =[5, 7, 10, 14, 19, 25, 32] 
    uw1=np.unwrap(l1, discont = -1*math.pi)
    print("Result 1: ", uw1) 
  
    l2 =[0, 1.34237486723, 4.3453455, 8.134654756, 9.3465456542] 
    uw2 = np.unwrap(l2, discont = math.pi)
    print("Result 2: ", uw2) 

    print('sub', diff(uw1,uw2))



