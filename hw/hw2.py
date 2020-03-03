import math

def Muller(xr, h, eps, maxit, func):
    x2 = xr
    x1 = xr + h*xr
    x0 = xr - h*xr
    count = 0
    #keep going until you find the loop
    while(True):
        count += 1
        h0 = x1 - x0
        h1 = x2 - x1
        d0 = (func(x1) - func(x0)) / h0
        d1 = (func(x2) - func(x1)) / h1
        a = (d1 - d0) / (h1 + h0)
        b = a*h1 + d1
        c = func(x2)
        rad = math.sqrt(b*b - 4*a*c)
        if (abs(b+rad) > abs(b-rad)):
            den = b + rad
        else:
            den = b - rad
        dxr = -2*c / den
        #finds the root
        xr = x2 + dxr
        #prints the root and the count
        print(count, xr)
        #breaks the loop if the count becomes larger than the max iteration
        if(abs(dxr) < eps*xror count >= maxit):
            return xr
        x0 = x1
        x1 = x2
        x2 = xr
        
def test_polynomial(x):
  return (x-3)*(x+2)*(x-1)

initial_root_guess = 4 # Guess root
relative_distance = 0.3 # Relative distance to other guesses
convergence_tolerance = 0.001
maximum_iterations = 100
Muller(initial_root_guess, relative_distance, convergence_tolerance, maximum_iterations, test_polynomial)
