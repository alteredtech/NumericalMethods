import numpy as np 

def rk4(x,y,h,derivs, params):
    ym = y.copy()
    ye = y.copy()
    n = len(y)
    slope = y.copy()
    ynew = y.copy()
    k1 = derivs(x, y,params)
    for i in range(n):
        ym[i] = y[i] + k1[i] * h / 2
    k2 = derivs(x + h / 2, ym,params)
    for i in range(n):
        ym[i] = y[i] + k2[i] * h /2
    k3 = derivs(x + h / 2, ym,params)
    for i in range(n):
        ye[i] = y[i] + k3[i] * h
    k4 = derivs(x + h, ye,params)
    for i in range(n):
        slope[i] = (k1[i] + 2*(k2[i] + k3[i]) + k4[i]) / 6
        ynew[i] = y[i] + slope[i] * h
    print(ynew)
    return ynew

def unwrap(dq):
    dqq = np.unwrap([dq])
    return dqq[0]

def getstate(bot):
    s = bot["state"]
    return [s["x"], s["y"], s["yaw"], s["vx"], s["vy"]]

def setstate(bot,s):
    bot["state"]["x"] = s[0]
    bot["state"]["y"] = s[1]
    bot["state"]["yaw"] = s[2]
    bot["state"]["vx"] = s[3]
    bot["state"]["vy"] = s[4]

def controller(bot,goalx,goaly):
    dx = goalx - bot["state"]["x"]
    dy = goaly - bot["state"]["y"]
    dq = unwrap(np.arctan2(dy,dx) - bot["state"]["yaw"])
    dl = np.sqrt(dx*dx + dy*dy)
    cq = np.cos(bot["state"]["yaw"])
    sq = np.sin(bot["state"]["yaw"])
    body_frame_velocity = bot["state"]["vx"]*cq + bot["state"]["vy"]*sq
    if dl > 1:
        bot["wheel_torque"] = max(-2,min(2,dl - body_frame_velocity))
        bot["steer_angle"] = max(-0.55,min(0.55,dq))
    else:
        bot["wheel_torque"] = -body_frame_velocity
        bot["steer_angle"] = 0

def plant(t,z,bot):
    setstate(bot,z)
    speed = np.sqrt(bot["state"]["vx"]*bot["state"]["vx"] + bot["state"]["vy"]*bot["state"]["vy"])
    cq = np.cos(bot["state"]["yaw"])
    sq = np.sin(bot["state"]["yaw"])
    body_frame_velocity = cq*bot["state"]["vx"] + sq*bot["state"]["vy"]
    yaw_rate = body_frame_velocity*np.tan(bot["steer_angle"])/bot["wheel_base"]
    Faero = -bot["drag_coefficient"]*speed*body_frame_velocity
    Fprop = bot["wheel_torque"]/bot["wheel_radius"]
    acceleration = (Fprop + Faero)/bot["mass"]
    ax = acceleration*cq - sq*body_frame_velocity*yaw_rate
    ay = acceleration*sq + cq*body_frame_velocity*yaw_rate
    return [bot["state"]["vx"], bot["state"]["vy"], yaw_rate, ax, ay]

def simulate(tstart, tend, h, bot, goal):
    y = getstate(bot)
    n = int((tend-tstart)/h)+1
    with open('out.txt','w') as w:
        for ii in range(n):
            t = tstart + ii*h
            y = rk4(t,y,h,plant,bot)
            setstate(bot,y)
            controller(bot, goal["x"], goal["y"])
            v = np.sqrt(bot['state']['vx']*bot['state']['vx'] + bot['state']['vy']*bot['state']['vy'])
            w.write("{} {} {} {} {} {}\n".format(t,bot['state']['x'],bot['state']['y'],v,bot['wheel_torque'],bot['steer_angle']))
            print(bot["state"]["x"],bot["state"]["y"])