def run(t0,v0,dt,tfinal,g,c,m):
    t = t[0]
    v = v[0]
    while t0 < tfinal:
        t0 += dt
        v0 += (g-c/m *v0)*dt
        t.append(t0)
        v.append(v0)
    return(t,v)

def taylor(derivs,h):
    val = 0
    fact = 1
    for i in range(len(derivs)):
        if i > 0:
            fact = fact*i

        val += derivs[0]/fact*np.pow(h,i)