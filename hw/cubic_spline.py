import numpy as np 

def cubic_spline(x,y):
    (A,r) = tridiag(x,y)
    d2x=np.linalg.solve(A,r)
    d2x = [0] + d2x.tolist() + [0]
    return d2x
    
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
            t1 = -3*c1*(x[i]-xu)**2
            t2 = 3*c2*(xu-x[i-1])**2
            t3 = -c3
            t4 = c4
            dy = t1 + t2 + t3 + t4
            t1 = 6 * c1 * (x[i] - xu)
            t2 = 6 * c2 * (xu - x[i-1])
            d2y = t1 + t2
            return (yu,dy,d2y)
    return (0,0)

def tridiag(x,y):
    arrSize = len(x)-2
    Arr = np.zeros([arrSize,arrSize])
    r = np.zeros([arrSize])
    for i in range(len(Arr)):
        print(Arr)
        j = i+1
        lenx = len(x)
        d1 = (x[i+1]-x[i])
        d2 = (x[j+1]-x[j])
        y1 = (y[i+1]-y[i])
        y2 = (y[j+1]-y[j])
        if i == 0:
            Arr[i,i]=2*(d1+d2)
            Arr[i,i+1]=d2
        elif i==len(Arr)-1:
            Arr[i,i-1]=(d1)
            Arr[i,i]=2*(d1+d2)
        else:
            Arr[i,i-1]=(d1)
            Arr[i,i]=2*(d1+d2)
            Arr[i,i+1]=(d2)
        r[i] = 6*((y2/d2)-(y1/d1))
    return Arr,r

if __name__ == '__main__':
  x = [3,4.5,7,9]
  y = [2.5,1,2.5,0.5]
  d2x = cubic_spline(x,y)
  print(d2x)