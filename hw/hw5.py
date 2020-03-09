

def linear_regression(x,y):
    sumx = 0
    sumy = 0
    sumxy = 0
    sumx2 = 0
    st = 0
    sr = 0
    n = len(x)
    for i in range(n):
        sumx = sumx + x[i]
        sumy = sumy + y[i]
        sumxy = sumxy + x[i]*y[i]
        sumx2 = sumx2 + x[i]*x[i]
    xm = sumx/n
    ym = sumy/n
    a1 = (n*sumxy - sumx*sumy)/(n*sumx2-sumx*sumx)
    a0 = ym - a1*xm
    for i in range(n):
        st = st + (y[i] - ym)**2
        sr = sr + (y[i] - a1*x[i] - a0)**2
    syx = (sr/(n-2))**0.5
    r2 = (st-sr)/st
    return(a0, a1, syx, r2)


if __name__ == '__main__':
  x = [1,2,3,4,5,6,7]
  y = [0.5,2.5,2.0,4.0,3.5,6.0,5.5]
  (a0,a1,syx,r2) = linear_regression(x,y)
  print(a0,a1,syx,r2)