# Newton fractals
# FB - 201003291
from PIL import Image
import math
imgx = 300
imgy = 300
image = Image.new("HSV", (imgx, imgy))

# drawing area
xa = -1.0
xb = 1.0
ya = -1.0
yb = 1.0

maxIt = 40 # max iterations allowed
h = 1e-6 # step size for numerical derivative
eps = 1e-3 # max error allowed

# put any complex function here to generate a fractal for it!
o_end = 10
o_frames = 50
start = 0
stop = math.pi
frames = 100

def f(z,fr,fr2):
    return z*z*1/math.tan(abs(z)-fr)-(fr2+2)
    # return z*z*z+math.cos(abs(z))-1
    # math.cos(abs(z)/2*math.pi)

# draw the fractal
for _ord in range(o_frames):
    o_step = _ord*float(o_end)/float(o_frames)
    for _i in range(frames):
        print(_ord,"/",o_frames,"\t-\t",_i,"/",frames)
        step = _i*float(stop)/float(frames)
        for y in range(imgy):
            zy = y * (yb - ya) / (imgy - 1) + ya
            for x in range(imgx):
                zx = x * (xb - xa) / (imgx - 1) + xa
                z = complex(zx, zy)
                for i in range(maxIt):
                    # complex numerical derivative
                    dz = (f(z + complex(h, h),step,o_step) - f(z,step,o_step)) / complex(h, h)
                    z0 = z - f(z,step,o_step) / dz # Newton iteration
                    if abs(z0 - z) < eps: # stop when close enough to any root
                        break
                    z = z0
                image.putpixel((x, y), (int(float(i)/float(maxIt) * 255.0), 255, 255))
        image.convert("RGB").save("render/{0:0>4}-{1:0>4}.png".format(_ord, _i), "PNG")
