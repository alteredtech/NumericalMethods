import numpy as np

def rk4(x,y,h,derivs,params):
    return ...

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

if __name__ == '__main__':
    bot = {"state":{"x":0,"y":0,"yaw":0,"vx":0,"vy":0},
        "mass":1,"wheel_base":1,"drag_coefficient":1,"wheel_radius":0.1,
        "wheel_torque":1,"steer_angle":0.1}
    goal = {"x":-40, "y":10}
    simulate(0, 20, 0.1, bot, goal)
