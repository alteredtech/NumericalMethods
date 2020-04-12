import math 
def rk4(x,y,h,derivs):
    n = len(y)
    ymidpoint=[0 for e in range(n)]
    yend=[0 for e in range(n)]
    slope=[0 for e in range(n)]
    ynew=[0 for e in range(n)]
    k1 = derivs(x,y)
    for i in range(n):
        print("i")
        ymidpoint[i]=y[i] + k1[i]*h/2
    k2 = derivs(x+h/2,ymidpoint)
    for j in range(n):
        print("j")
        ymidpoint[j]=y[j] + k2[j]*h/2
    k3 = derivs(x+h/2,ymidpoint)
    for k in range(n):
        print("k")
        yend[k]=y[k]+k3[k]*h
    k4 = derivs(x+h,yend)
    for l in range(n):
        print("l")
        slope[l]=(k1[l]+2*(k2[l]+k3[l])+k4[l])/6
        ynew[l]=y[l] + slope[l]*h
    return ynew


if __name__ == '__main__':

    def derivs(t,y):
        temp=[0 for j in range(len(y))]
        for i in range(len(y)):
            temp[i] = y[i]*t*t - 1.1*y[i]
        return temp
    def actual(t): # (1/y)dy = (t2-1.1)*dt  ==> ln(y) = t^3/3 - 1.1t  ==>  y = exp(t^3/3 - 1.1t) + c
        return math.exp(t**3/3 - 1.1*t)

    y = [1,4]
    n = 5
    tlow = 0
    thigh = 2
    h = (thigh - tlow)/(n-1)
    for ii in range(n):
        t = tlow + ii*h
        print(t, y, actual(t))
        y = rk4(t,y,h,derivs)
        print(y)
