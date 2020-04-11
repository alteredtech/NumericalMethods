# def Simp38n(a,b,nint,func):
#     nint = max(1,float(int((nint+2)/3)))*3
#     h=(b-a)/nint
#     summ=0
#     for i in range(int(nint/3)):
#         x0 = func(a+i*3*h)
#         x1 = func(a+(i*3 + 1)*h)
#         x2 = func(a+(i*3 + 2)*h)
#         x3 = func(a+(i*3 + 3)*h)
#         summ += 3*h*((x0+3*(x1+x2)+x3)/8)
#         print(int(12.0)//3)
#     return summ
def Simp38n(a, b, nint, func):
    nint = max(1, float(int((nint + 2) / 3))) * 3
    h = (b - a) / nint
    y = []
    x = a
    for i in range(a, int(nint) + 2):
        y.append(func(x))
        x += h
    integral = []
    for j in range(0, int(nint) // 3):
        integral.append((3 * h) * ((y.pop(0) + 3 * y.pop(0) + 3 * y.pop(0) + y[0]) / 8))
    sum_ = int(sum(integral))
    return sum_
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