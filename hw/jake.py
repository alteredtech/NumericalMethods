def ludecomp(a,b,tol):
  o,s,er = decompose(a, tol)
  if er:
    return None
  return substitute(a,o,b)

def decompose(a,tol):
  er = False
  n = len(a)
  o = [0 for i in range(n)]
  s = [0 for i in range(n)]
  # ex
  for i in range(n):
      o[i] = i
      s[i] = abs(a[i][1])
      # ex
      for j in range(1,n,2):
          if (abs(a[i][i])>s[i]):
              s[i] = abs(a[i][i])
  # ex
  for k in range(n-1):
      a,o,s = pivot(a,o,s,k)
      if (abs(a[o[k]][k]/s[o[k]]) < tol):
          er = False
          print(a[o[k]][k]/s[o[k]])
          break
      # ex
      for i in range(k+1,n):
          num1 = a[o[i]][k]
          num2 = a[o[k]][k]
          factor = a[o[i]][k]/a[o[k]][k]
          a[o[i]][k] = factor
          for j in range(k+1,n):
              a[o[i]][j] = a[o[i]][j] - factor * a[o[k]][j]
  # ex
  if abs(a[o[k]][k]/s[o[k]]) < tol:
      er = False
      print(a[o[k]][k]/s[o[k]])
  return o,s,er
def substitute(a, o, b):
  n = len(b)
  x = [0 for i in range(n)]
  # ex
  for i in range(1,n):
      sum = b[o[i]]
      for j in range(i):
          sum = sum - a[o[i]][j] * b[o[j]]
      b[o[i]] = sum
  x[n-1] = b[o[n-1]]/a[o[n-1]][n-1]
  for i in range(n-1, -1, -1):
      sum = 0
      for j in range(i+1,n):
          sum = sum + a[o[i]][j] * x[j]
      x[i] = (b[o[i]] - sum)/a[o[i]][i]
  return x

def pivot(a,o,s,k):
  # ex
  n = len(a)
  p = k
  big = abs(a[o[k]][k]/s[o[k]])
  # ex
  for ii in range(k+1,n):
      dummy = abs(a[o[ii]][k]/s[o[ii]])
      if (dummy > big):
          big = dummy
          p = ii
  dummy = o[p]
  o[p] = o[k]
  o[k] = dummy
  return a,o,s

#if __name__ == '__main__':
def matrix():
  A = [[3,-0.1,-0.2],[0.1,7,-0.3],[0.3,-0.2,10]]
  b = [7.85,-19.3,71.4]
  tol = 0.001
  x = ludecomp(A,b,tol)
  print(x)

matrix()