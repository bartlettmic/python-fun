#!/usr/bin/env python
from pydub import AudioSegment
from PIL import Image
from multiprocessing import Process, Pool, Manager, cpu_count
from time import sleep
import math, cmath, sys, os, inspect, re

# Mutual parameters across all processes
filename = "./"+sys.argv[1]
extension = sys.argv[1].split('.')[1]

# Audio buffer from given audio file
song = AudioSegment.from_file(filename, format=extension)
samples = song.get_array_of_samples()
sampleSize = len(samples)

#f(z) and df(z) to be used in newtonion iteration
def f(z,_i,loudness):
    return abs(z**(2+_i))-z**16-1+cmath.log(abs(z**(4)))
def df(z,_i,loudness):
    return 8*z**(3+_i)-z**(0.5*loudness**0.25)-(16)*z**(15)-1

# Record the functions used in the directory name
funcs = []
for _f in [f, df]:
    funcs.append(' '.join(re.split(r'\n', inspect.getsource(_f))[1].replace("return ","").replace("**","^").replace("*",u"\u00D7").replace("/",u"\u00F7").replace("_i","i").replace("cmath.","").replace("math.","").split()))
folder = "./render/" + " _ ".join(funcs)
if not os.path.exists(folder):
    os.makedirs(folder)
del funcs

# User-defined parameters #####################################################
imgx = 1280 #Image dimensions
imgy = 720
image = Image.new("HSV", (imgx, imgy))

xa = -1.28
xb =  1.28
ya = -1.0 # Domain of graph, scaled to dimensions
yb =  1.0

maxIt = 40 # max iterations allowed
eps = 0.05 # max error allowed

fps = 120.0  # Frames per second
Mstep = 0.005    #Size to step through f() and/or df() each frame
frames = int(math.ceil(fps*len(song) / 1000.0)) #total frames to be rendered
Sstep = sampleSize/frames   #Step size to synchronize audio-levels with frames

# Create a smaller array with just the audio levels we'll be referencing,
#   and normalize the audio to ratios instead of levels
vols = []
maxVol = 0;
_temp = 0
while _temp < sampleSize: #Float step isn't allowed in for-loop   
    vols.append(samples[int(_temp)])
    if samples[int(_temp)] > maxVol:
        maxVol = samples[int(_temp)]
    _temp += Sstep
del _temp
maxVol = (maxVol+song.max)/2

def render(start, stop, jobID,q):
    # sample = start*Sstep
    _i = start*Mstep
    for frame in range(start,stop):
        q[jobID-1] = ("{}: {}/{}".format(jobID,frame-start,stop-start))
        # loud=samples[int(sample)]/song.maxs
        loud = abs(vols[frame]/maxVol)
        for y in range(imgy):
            zy = y * (yb - ya) / (imgy - 1) + ya
            for x in range(imgx):
                zx = x * (xb - xa) / (imgx - 1) + xa
                z=complex(zy,zx)
                i=0
                while i < maxIt:
                    try:
                        dz = df(z,_i, loud)
                    except OverflowError:
                        pass
                    try:
                        z0 = (z - (f(z,_i,loud) / dz)) # Newton iteration
                    except OverflowError:
                        # pass
                        i+=1
                        continue
                    except ZeroDivisionError:
                        i+=1
                        continue
                    if abs(z0 - z) < eps: # stop when close enough to any root
                        break
                    z = z0
                    i+=1
                shadow = int((float(i)/float(maxIt))**2 * 255.0)
                image.putpixel((x, y), (255-shadow, 255, shadow*2))
        image.convert("RGB").save(folder+"/%04d.png" % frame, "PNG")
        # sample += Sstep
        _i+=Mstep
    q[jobID-1] = "{0}:{1}done{1}".format(jobID," "*len(str(stop)))
    return "\nDone."

if __name__ == '__main__':
    cores = cpu_count()
    pool = Pool(processes=cores) 
    q = Manager().list(['']*cores)
    print(frames,"frames over",cores,"cores;",imgx*imgy*frames,"total pixels.")
    res = None
    for job in range(cores):
        start = math.floor(job*frames/cores)
        stop = math.ceil((job+1)*frames/cores)
        res = pool.apply_async(render, (start,stop,job+1,q,))
    pool.close()
    while not res.ready():
        print(" | ".join(q),end="\r",flush=True)
        sleep(1)
    pool.join()
    print(res.get())
    pool.terminate()    
    
    image.convert("RGB").save(folder+"/_0.tiff", "PNG")
    
