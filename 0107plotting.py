import matplotlib.pyplot as plt 
import numpy as np 

m = 68.1 #kg
c = 12.5 #N/s "Constant"
g = 9.81 #m/s**2
finalTime = 20 #s

t = np.linspace(0,finalTime, 10)

v = g*m/c*(1-np.exp(-c/m*t))

fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(t,v,'b.-') #returns a tuple of line objects
line2, = ax.plot([t[0],t[0]],[v[0],v[0]],'r.-')

deltaTime = 2.0
tnow = t[0]
vnow = v[0]
for ii in range(int(finalTime/deltaTime)):
    tnext = tnow + deltaTime
    vnext = vnow + (g - c/m*vnow)*(tnext-tnow)
    vnow = vnext
    tnow = tnext
    line2.set_xdata(np.append(line2.get_xdata(), tnow))
    line2.set_ydata(np.append(line2.get_ydata(), vnow))
    fig.canvas.draw()
    fig.canvas.flush_events()
plt.show()