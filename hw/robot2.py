import math
def unwrap(dq):
  return ((dq+math.pi)%(2*math.pi))-math.pi

def rk4(x,y,h,derivs,params):
  n = len(y)
  k1 = derivs(x, y, params)
  ym = [y[ii] + k1[ii]*h/2 for ii in range(n)]
  k2 = derivs(x+h/2, ym, params)
  ym = [y[ii] + k2[ii]*h/2 for ii in range(n)]
  k3 = derivs(x+h/2, ym, params)
  ye = [y[ii] + k3[ii]*h for ii in range(n)]
  k4 = derivs(x+h, ye, params)
  return [y[ii] + ((k1[ii] + 2*(k2[ii]+k3[ii]) + k4[ii])/6)*h for ii in range(n)]

def getstate(bot):
  s = bot["state"]
  return [s["x"], s["y"], s["yaw"], s["vx"], s["vy"]]

def setstate(bot,s):
  bot["state"]["x"] = s[0]
  bot["state"]["y"] = s[1]
  bot["state"]["yaw"] = s[2]
  bot["state"]["vx"] = s[3]
  bot["state"]["vy"] = s[4]

def pathcontroller(bot):
  (en,eh,kff,dl) = bot['path'].nearest( bot['state']['x'], bot['state']['y'], bot['state']['yaw'])
  kd = 0.2*en + 1*eh + kff
  sa = math.atan(kd*bot['wheel_base'])
  bot['steer_angle'] = max(-0.55,min(0.55,sa))
  cq = math.cos(bot['state']['yaw'])
  sq = math.sin(bot['state']['yaw'])
  body_frame_velocity = bot['state']['vx']*cq+bot['state']['vy']*sq
  if dl > 1:
    bot['wheel_torque'] = max(-2, min(2, dl - body_frame_velocity))
  else:
    bot['wheel_torque'] = -0.5*body_frame_velocity

def controller(bot,goalx,goaly):
  dx = goalx - bot["state"]["x"]
  dy = goaly - bot["state"]["y"]
  dq = unwrap(math.atan2(dy,dx) - bot["state"]["yaw"])
  dl = math.sqrt(dx*dx + dy*dy)
  cq = math.cos(bot["state"]["yaw"])
  sq = math.sin(bot["state"]["yaw"])
  body_frame_velocity = bot["state"]["vx"]*cq + bot["state"]["vy"]*sq
  if dl > 1:
    bot["wheel_torque"] = max(-2,min(2,dl - body_frame_velocity))
    bot["steer_angle"] = max(-0.55,min(0.55,dq))
  else:
    bot["wheel_torque"] = -body_frame_velocity
    bot["steer_angle"] = 0

def plant(t,z,bot):
  setstate(bot,z)
  speed = math.sqrt(bot["state"]["vx"]*bot["state"]["vx"] + bot["state"]["vy"]*bot["state"]["vy"])
  cq = math.cos(bot["state"]["yaw"])
  sq = math.sin(bot["state"]["yaw"])
  body_frame_velocity = cq*bot["state"]["vx"] + sq*bot["state"]["vy"]
  yaw_rate = body_frame_velocity*math.tan(bot["steer_angle"])/bot["wheel_base"]
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
      pathcontroller(bot)
      v = math.sqrt(bot['state']['vx']*bot['state']['vx'] + bot['state']['vy']*bot['state']['vy'])
      w.write("{} {} {} {} {} {}\n".format(t,bot['state']['x'],bot['state']['y'],v,bot['wheel_torque'],bot['steer_angle']))
      print(bot["state"]["x"],bot["state"]["y"])

if __name__ == '__main__':
  from NumericalMethods.hw.SplinedPath import SplinedPath
  n = 20
  s = [5*ii/(n-1) for ii in range(n)]
  y = [10*math.cos(si) - 10 for si in s]
  x = [10*si + 4*math.sin(si) for si in s]
  path = SplinedPath(x,y)
  bot = {"state":{"x":0,"y":0,"yaw":0,"vx":0,"vy":0},
        "mass":1, "wheel_base":1, "drag_coefficient":1, "wheel_radius":0.1,
        "wheel_torque":1, "steer_angle":0.1, "path":path}
  goal = {"x":-40, "y":10}
  simulate(0, 20, 0.1, bot, goal)