import sys
import os
from PIL import Image
from numpy import array,dot,cross
from numpy.linalg import solve
from math import cos,sin,sqrt,pi
from fractions import Fraction

from numpy import seterr
seterr(all='raise')

# utility functions

width = 1500
xlist = [ float(2*u+1-width)/width for u in xrange(width) ]

def refl(vector,mir): return vector - 2*dot(vector,mir)*mir

def unit(vector):
        magnitude = sqrt(abs(dot(vector,vector)))
        return vector/magnitude

pqr = [ eval(s) for s in sys.argv[1:] ]
if len(pqr)>3:
        print "too many numbers; dropping last" 
        pqr = pqr[:3]
if sum([ Fraction(1,x) for x in pqr ]) >= 1:
        print "the reciprocals of the numbers must add to less than 1"
        while sum([ Fraction(1,x) for x in pqr ]) >= 1:
                pqr.pop()

filestem = ""
for n in pqr: filestem += repr(n)
while len(filestem) < 3:
        filestem += "i"

# make a list of mirror planes

if not pqr:     # all pairs are asymptotic
        ir3 = 1/sqrt(3)
        mirror = [ array([1j*ir3, 2*ir3, 0]),
                 array([1j*ir3, -ir3, -1]),
                 array([1j*ir3, -ir3, 1])]
else:
        p = pqr.pop(0)
        pangle = pi/p
        cosqr = [ -cos(pi/u) for u in pqr ]
        while len(cosqr) < 2: cosqr.append(-1)

        v0 = [0,1,0]
        v11 = -cos(pangle)
        v12 = sin(pangle)
        v1 = [ 0, v11, v12 ]
        v21 = cosqr[0]
        v22 = (cosqr[1] - v11*v21) / v12
        v2 = [ 1j*sqrt(abs(1-v21**2-v22**2)), v21, v22 ]
        mirror = [ array(v0), array(v1), array(v2) ]

        # Move everything so that the origin is equidistant from the mirror.

        #omnipoint = unit(solve(array(mirror), array([-1,-1,-1])))
        #if omnipoint[0].imag < 0: omnipoint = -omnipoint
        #tempmirror = unit(omnipoint - array([1j,0,0]))
        #for j,u in enumerate(mirror):
                #v = refl(u,tempmirror)
                #if v[0].imag <0: v = -v
                #mirror[j] = v

for u in mirror: print "mirror", u
v0,v1,v2 = mirror

# The meat!

def thecolor( x0,x1 ):
        r2 = x0**2 + x1**2
        if r2 >= 1: return (255,255,255,1)

        bottom = 1-r2
        p = array([ 1j*(1+r2)/bottom, 2*x0/bottom, 2*x1/bottom ])

        clean = 0
        while True:
                for j,u in enumerate(mirror):
                        if dot(p,u) > 0:
                                p = refl(p,u)
                                clean = 0
                        else:
                                clean += 1
                                if clean >= 3:
                                        #if dot(p,critplane) > 1: return (255,128,0,255)
                                        if abs(dot(p,v0)) < 0.185: return (0,0,255,255)
                                        if abs(dot(p,v1)) < 0.01: return (255,0,0,255)
                                        if abs(dot(p,v2)) < 0.01: return (0,255,64,255)
                                        return (0,0,0,255)


vertex = solve(array(mirror), array([0,1,1]))


vertex = solve(array(mirror), array([1,0,1]))

critplane = 1j*cross(vertex,v2)

im = Image.new("RGBA", (width,width) )
im.putdata( [ thecolor(x,y)
                for y in xlist
                for x in xlist
                ] )
im.save("H2lines_%s.png" % filestem)
print "done!"
