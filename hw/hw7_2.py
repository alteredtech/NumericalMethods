import numpy as np

def rEquation(x,y,i):
  return 6*((y[i+1] - y[i])/(x[i+1] - x[i]) - (y[i] - y[i-1])/(x[i] - x[i-1]))
  #6*((y[n-1]-y[n-2]))

def cubic_spline(x,y):
    (e,f,g,r) = tridiag(x,y)
    print(e,f,g,r)
    n = len(x)
    A = np.zeros([n-1,n-1])
    for i in range(n-1):
        if (i > 0): A[i,i-1] = e[i]
        A[i,i] = f[i]
        if (i < n-2): A[i,i+1] = g[i]
    print(A)
    A = np.delete(A,0,0)
    A = np.delete(A,0,1)
    r = np.delete(r,0)
    print(r)
    print(A)
    d2x = np.linalg.solve(A,r)
    # print(d2x)
    newtemp = A.tolist()
    print(newtemp,'newtemp')
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
    # r[n-2] = 6/(x[n-1]-x[n-2])*(y[n-1]-y[n-2])
    # r[n-2] = r[n-2] + 6/(x[n-2]-x[n-3])*(y[n-3]-y[n-2])
    return (e,f,g,r)

def interpolate(x,y,d2x,xu):
    n = len(x)
    for i in range(1,n):
        if xu >= x[i-1] and xu < x[i]:
            c1 = d2x[i-1]/6/(x[i]-x[i-1])
            c2 = d2x[i]/6/(x[i]-x[i-1])
            c3 = y[i-1]/(x[i]-x[i-1])-d2x[i-1]*(x[i]-x[i-1])/6
            c4 = y[i]/(x[i]-x[i-1])-d2x[i]*(x[i]-x[i-1])/6
            t1 = c1*(x[i]-xu)**3
            t2 = c2*(xu - x[i-1])**3
            t3 = c3*(x[i]-xu)
            t4 = c4*(xu - x[i-1])
            yu = t1 + t2 + t3 + t4
            return (yu,1)
    return (0,0)

if __name__ == '__main__':
  x = [3,4.5,7,9]
  y = [2.5,1,2.5,0.5]
  d2x = cubic_spline(x,y)