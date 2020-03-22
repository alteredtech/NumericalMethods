import numpy as np
import matplotlib.pyplot as plt

def general_linear_regression(A,q):
    #transpose the A array basically shift row to columns
    print(A,q)
    ATrans = np.transpose(A)
    print(ATrans)
    #does the dot product between A and A transpose
    a = np.dot(A,ATrans)
    #does the dot product between A and q
    b = np.dot(A,q)
    #solves for the z array
    print(a,len(a),len(a[0]))
    print(b,len(b))
    z=np.linalg.solve(a,b)
    print(z,"z")
    return z


if __name__ == '__main__':
    a0 = 0.1
    a1 = 2
    a2 = -3
    x = [0,1,2,3,4,5]
    y = [(a0+a1*xi+a1*xi*xi) for xi in x]
    n = len(x)
    A = [
        [1 for ii in range(n)],
        [xi*xi for xi in x]
        ]
    (z) = general_linear_regression(A,y)
    
    plt.title('plotting this data')
    plt.xlabel('x points')
    plt.ylabel('y points')
    plt.plot(x[:],y[:])
    plt.show