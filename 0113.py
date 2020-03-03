import matplotlib.pyplot as plt
import numpy as np

m = 68.1 # kg
g = 9.81 # m/s/s
v = 40
t = 20

def eval(c):
    return g*m/c*(1 - np.exp(-c/m*t))-v

min_c = 1
max_c = 25
c = np.linspace(min_c,max_c,10)
f = eval(c)
fig = plt.figure()
ax1 = fig.add_subplot(211)
line1, = ax1.plot(c, f, 'b.-') # Returns a tuple of line objects, thus the comma
ax2 = fig.add_subplot(212)
line2, = ax2.plot([0],[0], 'r.-')
c0 = min_c
f0 = eval(c0)
c1 = max_c
f1 = eval(c1)
if f0*f1 < 0:
    for i in range(20):
        plt.show()
        print(i)
        c2 = (c0+c1)/2
        f2 = eval(c2)
        line2.set_xdata(np.append(line2.get_xdata(),i))
        line2.set_ydata(np.append(line2.get_ydata(),f2))
        fig.canvas.draw()
        fig.canvas.flush_events()
        
        if f2 == 0:
            break
        elif np.sign(f0) == np.sign(f2):
            f0 = f2
            c0 = c2
        else:
            f1 = f2
            c1 = c2
