import numpy as np

def rEquation(x,y,i):
  return 6*((y[i+1] - y[i])/(x[i+1] - x[i]) - (y[i] - y[i-1])/(x[i] - x[i-1]))

def cubic_spline(x,y):
    (e,f,g,r) = tridiag(x,y)
    print(e,f,g,r)
    n = len(x)
    A = np.zeros([n-1,n-1])
    for ii in range(n-1):
        if (ii > 0): A[ii,ii-1] = e[ii]
        A[ii,ii] = f[ii]
        if (ii < n-2): A[ii,ii+1] = g[ii]
    print(A)
    A = np.delete(A,0,0)
    A = np.delete(A,0,1)
    r = np.delete(r,0)
    print(r)
    print(A)
    d2x = np.linalg.solve(A,r)
    d2x = [0] + d2x.tolist() + [0]
    return d2x

def tridiag(x,y):
    n = len(x)
    e=np.zeros(n-1)
    f=np.zeros(n-1)
    g=np.zeros(n-1)
    r=np.zeros(n-1)
    f[0]=2*(x[2]-x[0])
    g[0]=(x[2]-x[1])
    r[0]=rEquation(x,y,1)
    # print(e,f,g,r,n)
    for i in range(1,n-2):
        e[i] = (x[i]-x[i-1])
        g[i] = (x[i+1]-x[i])
        f[i] = 2 * (x[i+1]-x[i-1])
        r[i] = rEquation(x,y,i)
    e[n-2] = (x[n-2]-x[n-3])
    f[n-2] = 2 * (x[n-1]-x[n-3])
    r[n-2] = rEquation(x,y,n-2)
    return (e,f,g,r)