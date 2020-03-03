def Ludecomp (a, b, tol):
    o,s,er = Decompose(a,tol)
    if er:
        return None
    return Substitute(a, o, b)

def Decompose (a, tol):
    er = False
    n = len(a)
    o = [0 for i in range(n)]
    s = [0 for i in range(n)]
    #0,2 (1,n)
    for i in range(n):
        #set num to row number
        o[i] = i
        s[i] = abs(a[i][1])
        # 0,2 (2,n)
        for j in range(1,n,2):
            if (abs(a[i][i])>s[i]):
                s[i] = abs(a[i][i])
    #0,2 (1,n-1)
    for k in range(n-1):
        a,o,s = Pivot(a,o,s,k)
        if (abs(a[o[k]][k]/s[o[k]]) < tol):
            er = False
            print(a[o[k]][k]/s[o[k]])
            break
        #1,2 (k+1,n)
        for i in range(k+1,n):
            num1 = a[o[i]][k]
            num2 = a[o[k]][k]
            factor = a[o[i]][k]/a[o[k]][k]
            a[o[i]][k] = factor
            #0,2 (k+1,n)
            for j in range(k+1,n):
                a[o[i]][j] = a[o[i]][j] - factor * a[o[k]][j]
    num = abs(a[o[k]][k]/s[o[k]])
    if (num < tol):
        er = False
    return o,s,er
def Substitute (a, o, b):
    n = len(b)
    x = [0 for i in range(n)]
    #forsub
    #0,2 (2,n)
    for i in range(1,n):
        sum = b[o[i]]
        #(1,i-1)
        for j in range(i):
            sum = sum - a[o[i]][j] * b[o[j]]
        b[o[i]] = sum
    x[n-1] = b[o[n-1]]/a[o[n-1]][n-1]
    #backsub
    #2,0,-1 (n-1,1)
    for i in range(n-1, -1, -1):
        sum = 0
        #(i+1,n)
        for j in range(i+1,n):
            sum = sum + a[o[i]][j] * x[j]
        x[i] = (b[o[i]] - sum)/a[o[i]][i]
    return x     

def Pivot (a, o, s, k):
    n = len(a)
    p = k
    big = abs(a[o[k]][k]/s[o[k]])
    #k+1,2 (k+1,n)
    for ii in range(k+1,n):
        dummy = abs(a[o[ii]][k]/s[o[ii]])
        if (dummy > big):
            big = dummy
            p = ii
    dummy = o[p]
    o[p] = o[k]
    o[k] = dummy
    return a,o,s



def matrix():
        A = [[3,-0.1,-0.2],[0.1,7,-0.3],[0.3,-0.2,10]]
        b = [7.85,-19.3,71.4]
        tol = 0.001
        x = Ludecomp(A,b,tol)
        print(x)

matrix()
