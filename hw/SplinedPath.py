import math
import numpy as np 

class SplinedPath:
    def __init__(self, x, y):
        self.currentseg = 1
        self.x = x
        self.y = y
        self.s = [0] # Not really path length but something related to it.
        for ii in range(1,len(x)):
            dx = x[ii] - x[ii-1]
            dy = y[ii] - y[ii-1]
            self.s.append(self.s[-1] + math.sqrt(dx*dx+dy*dy))
        self.d2x = cubic_spline(s,x)#TODO Get the second derivative of the cubic spline x(s) at each knot (remember first and last should be zero)
        self.d2y = cubic_spline(s,y)#TODO Get the second derivative of the cubic spline y(s) at each knot (remember first and last should be zero)
    
    def nearest(self,botx,boty,botyaw):
        en = 0  # Normal error (perpendicular distance from botx,boty to the nearest point on the cubic spline path)
        eh = 0  # Heading error (angular distance from the robots heading (botyaw) to the path heading)
        kff = 0 # Curvature of the cubic splined path (we'll also call it the feedforward curvature kff)
        length_remaining = 0
        Ltot = self.s[-1] # Total path length (roughly)
        for jj in range(self.currentseg,len(self.x)-1):
            # Vector from jjth knot and (jj+1)th knot
            segv = [self.x[jj+1] - self.x[jj], self.y[jj+1] - self.y[jj]]
            # Vector from jjth knot to the robot
            botv = [botx         - self.x[jj], boty         - self.y[jj]]
            # What percent of the way between the jjth and (jj+1)th knot is the robot?
            prcnt = (segv[0]*botv[0]+botv[1]*segv[1])/(segv[0]*segv[0]+segv[1]*segv[1])
            if prcnt < 1: # If it is less than 1 then we assume we are on this segment
                self.currentseg = jj # Set the current segment to jj so we never look again at segments we've already passed
                # Finally, we can get the value of the independent parameter "s" that represents the nearest point to the robot
                ss = self.s[jj] + prcnt*(self.s[jj+1]-self.s[jj])
                # How much "length" is left on the path?
                length_remaining = Ltot - ss
                if ss < Ltot:#TODO make sure ss is in range if it is then
                    #TODO Get x(ss), dxds(ss), d2xds2(ss)
                    xu,dxds,d2xds2 = interpolate(ss,x,d2x,length_remaining)
                    #TODO Get y(ss), dyds(ss), d2yds2(ss)
                    yu,dyds,d2yds2 = interpolate(ss,y,d2y,length_remaining)
                    q = math.atan2(dyds,dxds)#TODO, get the path heading HINT: all you need are dxds and dyds
                    qp = q-math.pi/2 # This is going to point perpendicularly to the right of the direction of travel along the path
                    en = (botx-x(ss))*math.cos(qp) + (boty-y(ss))*math.sin(qp)# TODO Normal error ==> (botx-x(ss))*math.cos(qp) + (boty-y(ss))*math.sin(qp)
                    eh = np.unwrap(q-botyaw,math.pi) - np.unwrap(q-botyaw,-1*math.pi) # TODO unwrap(q-botyaw) <== unwrap to between -pi and pi
                    kff = abs(dxds*d2yds2-dyds*d2xds2)/(dxds**2-dyds**2)**(2/3) # Curvature of the path. You will find the formula for this under the sub-topic "In terms of a general parameterization" at https://en.wikipedia.org/wiki/Curvature You will need dxds(ss), d2xds2(ss), dyds(ss), and d2yds2(ss)
                break
        return (en,eh,kff,length_remaining)


def cubic_spline(x,y):
    (A,r) = tridiag(x,y)
    d2x=np.linalg.solve(A,r)
    d2x = [0] + d2x.tolist() + [0]
    return d2x
    
def interpolate(x,y,d2x,xu):
    n = len(x)
    for i in range(1,n):
        if xu >= x[i-1] and xu < x[i]:
            c1 = d2x[i-1]/6/(x[i]-x[i-1])
            c2 = d2x[i]/6/(x[i]-x[i-1])
            c3 = y[i-1]/(x[i]-x[i-1])-d2x[i-1]*(x[i]-x[i-1])/6
            c4 = y[i]/(x[i]-x[i-1])-d2x[i]*(x[i]-x[i-1])/6
            t1 = c1*(x[i]-xu)**3
            t2 = c2*(xu - x[i-1])**3
            t3 = c3*(x[i]-xu)
            t4 = c4*(xu - x[i-1])
            yu = t1 + t2 + t3 + t4
            t1 = -3*c1*(x[i]-xu)**2
            t2 = 3*c2*(xu-x[i-1])**2
            t3 = -c3
            t4 = c4
            dy = t1 + t2 + t3 + t4
            t1 = 6 * c1 * (x[i] - xu)
            t2 = 6 * c2 * (xu - x[i-1])
            d2y = t1 + t2
            return (yu,dy,d2y)
    return (0,0)

def tridiag(x,y):
    arrSize = len(x)-2
    Arr = np.zeros([arrSize,arrSize])
    r = np.zeros([arrSize])
    for i in range(len(Arr)):
        print(Arr)
        j = i+1
        lenx = len(x)
        d1 = (x[i+1]-x[i])
        d2 = (x[j+1]-x[j])
        y1 = (y[i+1]-y[i])
        y2 = (y[j+1]-y[j])
        if i == 0:
            Arr[i,i]=2*(d1+d2)
            Arr[i,i+1]=d2
        elif i==len(Arr)-1:
            Arr[i,i-1]=(d1)
            Arr[i,i]=2*(d1+d2)
        else:
            Arr[i,i-1]=(d1)
            Arr[i,i]=2*(d1+d2)
            Arr[i,i+1]=(d2)
        r[i] = 6*((y2/d2)-(y1/d1))
    return Arr,r