# Newton fractals
# FB - 201003291
from PIL import Image
import math
import cmath
from scipy.optimize import fsolve
imgx = 1000
imgy = 1000
image = Image.new("HSV", (imgx, imgy))
# drawing area
xa = -1.0
xb = 1.0
ya = -1.0
yb = 1.0
 
maxIt = 40 # max iterations allowed
h = 1e-6 # step size for numerical derivative
eps = 1e-3 # max error allowed
a = 1

def f(z):
    return z**3-1
    # return z**(5)+15*z**(4)-16
    # return z*z*z+math.cos(abs(z))-1
    # math.cos(abs(z)/2*math.pi)
 
# draw the fractal
print(fsolve(f,1))
_i = 0
frame = 0
step = 0.1
while 1:
    print(_i," : ",frame)
    # stdout.flush()
    for y in range(imgy):
        zy = y * (yb - ya) / (imgy - 1) + ya
        for x in range(imgx):
            zx = x * (xb - xa) / (imgx - 1) + xa
            z = complex(zx, zy)
            i=0
            while i < maxIt:
                # complex numerical derivative
                # dz = (f(z + complex(h, h),_i) - f(z,_i)) / complex(h, h)
                # if (dz == 0):
                    # i+=1
                    # continue
                dz = 3*z**2
                z0 = z - a*(f(z) / dz) # Newton iteration
                if abs(z0 - z) < eps: # stop when close enough to any root
                    break
                z = z0
                i+=1
            color = 32
            if abs(1-z) < 1:
                color = 0
            # if abs(-1-z) < 1:
            #     color = 63
            # if abs(complex(0,1)-z) < 1:
            #     color = 127
            # if abs(complex(0,-1)-z) < 1:
            #     color = 191
            
            if abs(complex(-0.5,0.86)-z) < 1:
                color = 85
            if abs(complex(-0.5,-0.86)-z) < 1:
                color = 170
            ratio = int(float(i)/float(maxIt) * 255.0)
            image.putpixel((x, y), (color, 255, 255-ratio*2))
    image.convert("RGB").save("render/%04d.png" % frame, "PNG")
    _i+=step
    frame += 1