import math
def brentsopt(x1, xu,f):
    # doing all the setting
    tol = 0.000001
    phi = (1 + math.sqrt(5))/2
    rho = 2 - phi
    u = x1 + rho*(xu - x1)
    v = u
    w = u
    x = u
    fu = f(u)
    fv = fu
    fw = fu
    fx = fu
    xm = 0.5*(x1 + xu)
    d = 0
    e = 0
    count = 0
    #keep going untill 10k then break
    while(count < 10000):
        if abs(x - xm) <= tol:
            break
        para = abs(e) > tol
        if para: #(Try parabolic fit)
            r = (x - w)*(fx - fv)
            q = (x - v)*(fx - fw)
            p = (x - v)*q - (x - w)*r
            s = 2*(q - r)
            if s > 0:
                p = -p
            s = abs(s) # Is the parabola acceptable? 
            para = abs(p) < abs(0.5*s*e) and p > s*(x1 - x) and p < s*(xu - x)
            if para:
                e = d
                d = p/s #(Parabolic interpolation step)
        if not para:
            if x >= xm: #(Golden-section search step)
                e = x1 - x
            else:
                e = xu - x
            d = rho*e
        u = x + d
        fu = f(u)
        if fu <= fx: #(Update x1, xu, x, v, w, xm)
            if u >= x:
                x1 = x
            else:
                xu = x
            v = w
            fv = fw
            w = x
            fw = fx
            x = u
            fx = fu
        else:
            if u < x:
                x1 = u
            else:
                xu = u
            if fu <= fw or w == x:
                v = w
                fv = fw
                w = u
                fw = fu
            elif fu <= fv or v == x or v == w:
                v = u
                fv = fu
        xm = 0.5*(x1 + xu)
        count+=1
    return u


def func(x):
  return 2*x + 3./x

if __name__ == '__main__':
    u = brentsopt(0,20,func)
    print(math.sqrt(3/2))
    print(u,func(u))

