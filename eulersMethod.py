# import matplotlib.pyplot as plt 
# import numpy as np 
# import predict

# m = 68.1 #kg
# c = 12.5 #N/s "Constant"
# g = 9.81 #m/s**2
# finalTime = 20 #s
# deltaTime = 2
# tnow = t[0]
# vnow = v[0]

# t=np.linspace(0,finalTime,20)
# v = g*m/c*(1-np.exp(-c/m*t))

# (tPredict,vPredict) = predict.run(t[0],v[0],deltaTime,finalTime,g,c,m)

# error = []
# for i in range(len(tPredict)):
#     vActual = g * m /c * (1-np.exp(-c/m*tPredict[i]))
#     error.append((vActual - vPredict[i]))

global = 1