# Newton fractals
# FB - 201003291
from PIL import Image
import math
import cmath
#from mpmath import findroot
from scipy.misc import derivative

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
eps = 1e-2 # max error allowed
a = -0.5

def f(z,_i):
    return z**(8*math.sin(_i/math.pi*2))-z**16-_i
def df(z,_i):
    return 8*z**(4*math.sin(_i/math.pi*2))-16*z**15-_i
    

frame=0
step=0.1
_i = 0
while True:
    for y in range(imgy):
        zy = y * (yb - ya) / (imgy - 1) + ya
        for x in range(imgx):
            zx = x * (xb - xa) / (imgx - 1) + xa
            z = complex(zy, zx)
            i=0
            while i < maxIt:
                # dz = (f(z + complex(h, h)) - f(z)) / complex(h, h)
                try:
                    dz = df(z,_i)
                except OverflowError:
                    pass
                try:
                    z0 = z - (f(z,_i) / dz) # Newton iteration
                except OverflowError:
                    pass
                if abs(z0 - z) < eps: # stop when close enough to any root
                    break
                z = z0
                i+=1
            shadow = int((float(i)/float(maxIt))**2 * 255.0)
            image.putpixel((x, y), (255-shadow, 255, shadow*2))
        print(frame,":",round(_i,1),"\t",round(y/imgy*100),"%", end='\r',flush=True)
    image.convert("RGB").save("render/%04d.png" % frame, "PNG")
    _i+=step
    frame += 1
