import math

def func(x):
    return math.sin(x)+math.cos(1+x**2)-1

def false():
    xl = -2
    xu = 2
    for i in range(2):
        xr = xu-(func(xu)*(xl-xu)/(func(xl)-func(xu)))
        print('value of xr '+str(xr))
        temp = func(xr)*func(xl)
        print('value of temp '+str(temp))
        if temp < 0:
            xu = xr
        elif temp > 0:
            xl = xr
        else:
            break

def scant():
    print(math.radians(math.sin(30)))
    print(math.radians(math.cos(30)))
    x = [-2,2]
    for i in range(1,6):
        x.append(x[i]-(func(x[i])*(x[i-1]-x[i])/(func(x[i-1])-func(x[i]))))
        print(x[i])

scant()

