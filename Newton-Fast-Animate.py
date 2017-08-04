from PIL import Image
import math, cmath, sys, os, inspect, re, atexit

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

def f(z,_i):
    return z**(2+_i)-z**16-1+cmath.log(abs(2*z**(1+_i)
    # return z**(8*math.sin(_i/math.pi*2))-z**16-_i
def df(z,_i):
    return 8*z**(3+_i)-16*z**15-_i
    # return 8*z**(4*math.sin(_i/math.pi))-16*z**15-_i

# Record the functions used in the directory name
funcs = []
for _f in [f, df]:
    funcs.append(re.split(r'\s+|\n', inspect.getsource(_f))[3].replace("**","^").replace("*",u"\u00D7").replace("/",u"\u00F7").replace("_i","i").replace("cmath.","").replace("math.",""))
folder = "./render/" + " _ ".join(funcs)

if not os.path.exists(folder):
    os.makedirs(folder)
    
def make_tiff():
    image.convert("RGB").save(folder+"/_0.tiff", "PNG")
atexit.register(make_tiff)

start=0
frame=start
step=0.01
_i = 0+start*step
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
                except ZeroDivisionError:
                    i+=1
                    continue
                if abs(z0 - z) < eps: # stop when close enough to any root
                    break
                z = z0
                i+=1
            shadow = int((float(i)/float(maxIt))**2 * 255.0)
            image.putpixel((x, y), (255-shadow, 255, shadow*2))
        print(frame,":",round(_i,3),"\t",round(y/imgy*100),"%", end='\r',flush=True)
    image.convert("RGB").save(folder+"/%04d.png" % frame, "PNG")
    _i+=step
    frame += 1
