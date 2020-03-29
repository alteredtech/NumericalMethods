def Simp38n(a,b,nint,func):
    nint = max(1,float(int((nint+2)/3)))*3 # Make this change to nint to ensure that the intervals are a multiple of 3
    #... apply the Simpson's 3/8 rule over the appropriate intervals to get an estimate of the integral
    #... for example if nint = 3 you will apply Simpson's 3/8 rule once.
    h=(b-a)/nint
    nint = int(nint/3)
    summ=0
    for i in range(nint):
        print(i,summ)
        if i ==0:
            x0=func(0)#0
            x1=func(h)#1
            x2=func(h*2)#2
            x3=func(h*3)#3
        else:
            x0=func(h)#4
            x1=func(h*2)#5
            x2=func(h*3)#6
            x3=func(h*4)#7
        summ +=3*h*((x0+3*x1+3*x2+x3)/8)
        h=h*5
    return summ

if __name__ == "__main__":
    def func(x):
        return 3*x**2 - 2*x - 4
    def ifunc(x):
        return x**3 - x**2 - 4*x 
    a = 1
    b = 4
    nint = 10
    est_integral = Simp38n(a,b,nint,func)
    true_integral = ifunc(b) - ifunc(a)

    print(est_integral,true_integral)