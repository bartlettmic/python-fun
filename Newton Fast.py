# Newton fractals
# FB - 201003291
from PIL import Image
import math
import cmath
#from mpmath import findroot
# from scipy.misc import derivative

def truncate(number, digits) -> float:
    stepper = pow(10.0, digits)
    return math.trunc(stepper * number) / stepper
imgx = 500
imgy = 500
image = Image.new("HSV", (imgx, imgy))
# drawing area
xa = -1.0
xb = 1.0
ya = -1.0
yb = 1.0
 
maxIt = 40 # max iterations allowed
h = 1e-6 # step size for numerical derivative
eps = 1e-3 # max error allowed
a = -0.5
roots=[]
matrix = [[0 for x in range(imgx)] for y in range(imgy)] 

def f(z):
    return z**8-z**16-1


#Find all the roots displayed in the image, essentially a pre-pass to expedite image creation
for y in range(imgy):
    zy = y * (yb - ya) / (imgy - 1) + ya
    for x in range(imgx):
        zx = x * (xb - xa) / (imgx - 1) + xa
        z = complex(zx, zy)
        i=0
        while i < maxIt:
            #dz = (f(z + complex(h, h)) - f(z)) / complex(h, h)
            dz = 8*z**7-16*z**15+z**(cmath.log(z))
            # dz = derivative(f, z)
            # z0 = z - a*(f(z) / dz) # Newton iteration
            z0 = z - (f(z) / dz) # Newton iteration
            if abs(z0 - z) < eps: # stop when close enough to any root
                break
            z = z0
            i+=1
        # _root = findroot(f,z, verify=False)
        # _root = complex(round(_root.real,3),round(_root.imag,3))
        _root = complex(round(z.real,3),round(z.imag,3))
        try:
            matrix[x][y] = [roots.index(_root),i]
        except:
            roots.append(_root)
            matrix[x][y] = [len(roots)-1,i]
    print(y)

# Create image now that we know how many roots there are
for y in range(imgy):
    for x in range(imgx):
        color = int(float(matrix[x][y][0]+1)/float(len(roots))*255.0)
        shadow = int((float(matrix[x][y][1])/float(maxIt))**2 * 255.0)
        # image.putpixel((x, y), (color, 255, 255-ratio*2))
        image.putpixel((x, y), (color, 255, shadow*2))
image.convert("RGB").save("fractal.png", "PNG")
