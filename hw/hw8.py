def Simp38n(a,b,nint,func):
    nint = max(1,float(int((nint+2)/3)))*3 # Make this change to nint to ensure that the intervals are a multiple of 3
    #... apply the Simpson's 3/8 rule over the appropriate intervals to get an estimate of the integral
    #... for example if nint = 3 you will apply Simpson's 3/8 rule once.
    h=(b-a)/nint
    m=h
    nint = int(nint/3)
    summ=0
    for i in range(nint):
        print(i,summ,h)
        # if i ==0:
        #     x0=func(0)#0
        #     x1=func(h)#1
        #     x2=func(h+m)#2
        #     x3=func(h+m+m)#3
        #     print(x0,x1,x2,x3)
        #     h+=m+m
        # else:
        #     x0=func(h)#4
        #     # print(h+m)
        #     x1=func(h+m)#5
        #     # print(h+m+m)
        #     x2=func(h+m+m)#6
        #     # print(h+m+m+m)
        #     x3=func(h+m+m+m)#7
        #     print(x0,x1,x2,x3)
        #     h+= m*3
        # summ +=(b-a)*((x0+3*x1+3*x2+x3)/8)
        x0 = func(a+i*3*h)
        x1 = func(a+(i*3 + 1)*h)
        x2 = func(a+(i*3 + 2)*h)
        x3 = func(a+(i*3 + 3)*h)
        print(x0,x1,x2,x3)
        summ += 3*h*((x0+3*(x1+x2)+x3)/8)
    return summ

if __name__ == "__main__":
    def func(x):
        return 3*x**2 - 2*x - 4
        #return 0.2 + 25*x - 200*x**2 + 675*x**3 - 900*x**4 + 400*x**5
    def ifunc(x):
        #return (200*x**6)/3-100*x**5+(675*x**4)/4-(200*x**3)/3+(25*x**2)/2+.2*x
        return x**3 - x**2 - 4*x 
    a = 1
    b = 4
    nint = 10
    est_integral = Simp38n(a,b,nint,func)
    true_integral = ifunc(b) - ifunc(a)

    print(est_integral,true_integral)