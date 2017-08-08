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
    # return z**(2+_i)-z**16-1+(cmath.log(abs(z**(1+_i))))
    # loudness = (-cmath.cos(_i*math.pi)/2 + 0.5)
    frac, whole = math.modf(_i/2.0+0.5)
    loudness = 2.0*abs(0.5 - frac)
    return (9*loudness+1)*z**(4)-(z**(16+_i/15.0))+(cmath.log(abs(z**(loudness*2.5))))-z**z
    # return z**((3))-(z**16)+(cmath.log(abs(2*z**(1+_i)))) - 1
def df(z,_i):
    frac, whole = math.modf(_i/2.0+0.5)
    loudness = 2.0*abs(0.5 - frac)
    return (z)**(5)-(16)*z**(15)-1

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

frame=0
step=0.1
_i = frame*step
# 11.5 MAX
while True:
    for y in range(imgy):
        zy = y * (yb - ya) / (imgy - 1) + ya
        for x in range(imgx):
            zx = x * (xb - xa) / (imgx - 1) + xa
            z = complex(zy, zx)
            __i = (1-math.cos(_i*(math.pi)))
            i=0
            while i < maxIt:
                try:
                    dz = df(z,_i)
                    # dz = (f(z + complex(h, h), _i) - f(z, _i)) / complex(h, h)
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
