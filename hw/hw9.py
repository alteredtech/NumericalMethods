import math 
def rk4(x,y,h,derivs):
    k1 = derivs(x,y)
    ymidpoint = y + k1*h/2
    k2 = derivs(x+h/2,ymidpoint)
    ymidpoint = y + k2*h/2
    k3 = derivs(x+h/2,ymidpoint)
    yend = y+k3*h
    k4 = derivs(x+h,yend)
    slope=(k1+2*(k2+k3)+k4)/6
    ynew = y + slope*h
    return ynew


#   SUBROUTINE ynew = rk4(x,y,h)
#   k1 = derivs(x,y)
#   ymidpoint = y + k1*h/2
#   k2 = derivs(x+h/2,ymidpoint)
#   ymidpoint = y + k2*h/2
#   k3 = derivs(x+h/2,ymidpoint)
#   yend = y + k3*h
#   k4 = derivs(x+h,yend)
#   slope = (k1 + 2*(k2+k3) + k4)/6
#   ynew = y + slope*h

if __name__ == '__main__':

    def derivs(t,y):
        return y*t*t - 1.1*y
    def actual(t): # (1/y)dy = (t2-1.1)*dt  ==> ln(y) = t^3/3 - 1.1t  ==>  y = exp(t^3/3 - 1.1t) + c
        return math.exp(t**3/3 - 1.1*t)

    y = 1
    n = 5
    tlow = 0
    thigh = 2
    h = (thigh - tlow)/(n-1)
    for ii in range(n):
        t = tlow + ii*h
        print(t, y, actual(t))
        y = rk4(t,y,h,derivs)
        print(y)