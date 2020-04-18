import math
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
        self.d2x = 1#TODO Get the second derivative of the cubic spline x(s) at each knot (remember first and last should be zero)
        self.d2y = 1#TODO Get the second derivative of the cubic spline y(s) at each knot (remember first and last should be zero)
    
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
                if 1==1:#TODO make sure ss is in range if it is then
                    #TODO Get x(ss), dxds(ss), d2xds2(ss)
                    #TODO Get y(ss), dyds(ss), d2yds2(ss)
                    q = 1#TODO, get the path heading HINT: all you need are dxds and dyds
                    qp = q-math.pi/2 # This is going to point perpendicularly to the right of the direction of travel along the path
                    en = 1# TODO Normal error ==> (botx-x(ss))*math.cos(qp) + (boty-y(ss))*math.sin(qp)
                    eh = 1# TODO unwrap(q-botyaw) <== unwrap to between -pi and pi
                    kff = # Curvature of the path. You will find the formula for this under the sub-topic "In terms of a general parameterization" at https://en.wikipedia.org/wiki/Curvature You will need dxds(ss), d2xds2(ss), dyds(ss), and d2yds2(ss)
            break
        return (en,eh,kff,length_remaining)