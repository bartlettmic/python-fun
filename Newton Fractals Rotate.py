# Newton fractals
# FB - 201003291
from PIL import Image
import math
import cmath
from mpmath import findroot
# from scipy.misc import derivative

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper
imgx = 100
imgy = 100
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
matrix = [[0 for x in range(imgx)] for y in range(imgy)] 

def f(z):
    return z**3-1

# Create image now that we know how many roots there are
frame = 0
step = 0.9
while 1:
    print(frame)
    roots=[]
    for y in range(imgy):
        zy = y * (yb - ya) / (imgy - 1) + ya
        for x in range(imgx):
            zx = x * (xb - xa) / (imgx - 1) + xa
            z = complex(zx, zy)
            i=0
            while i < maxIt:
                dz = (f(z + complex(h, h)) - f(z)) / complex(h, h)
                if (dz == 0):
                    i+=1
                    continue
                # dz = derivative(f, z)
                # z0 = z - a*(f(z) / dz) # Newton iteration
                z0 = z - (f(z) / dz) # Newton iteration
                if abs(z0 - z) < eps: # stop when close enough to any root
                    break
                z = z0
                i+=1
            _root = complex(round(z.real),round(z.imag))
            if _root not in roots:
                roots.append(_root)
            color = int(float(roots.index(_root))/float(len(roots))*255.0)
            shadow = int((float(i)/float(maxIt)) * 255.0)
            image.putpixel((x, y), (color, 255, shadow))
    image.convert("RGB").save("render/%04d.png" % frame, "PNG")
    frame += 1
    xa *= step
    xb *= step
    ya *= step
    yb *= step