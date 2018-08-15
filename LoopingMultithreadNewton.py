#!/usr/bin/env python
from pydub import AudioSegment
from PIL import Image
from multiprocessing import Process, Pool, Manager, cpu_count
from time import sleep, time
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
    return abs(z**(3.05+_i))-z**16-1+cmath.log(abs(z**(4)))
def df(z,_i,loudness):
    return (8+loudness)*z**(3+(1.75*_i))-(16)*z**(15)-(2-loudness)
    # return 8*z**(3+_i)-z-(16)*z**(15)-1
    # return 8*z**(3+_i)-z-(16)*z**(15)-(1+loudness)

# Record the functions used in the directory name
funcs = []
for _f in [f, df]:
    funcs.append(' '.join(re.split(r'\n', inspect.getsource(_f))[1].replace("return ","").replace("**","^").replace("*"," x ").replace("/"," div ").replace("33**_i","i").replace("cmath.","").replace("math.","").split()))
folder = "./render/" + " _ ".join(funcs)
if not os.path.exists(folder):
    os.makedirs(folder)
del funcs

# User-defined parameters #####################################################
imgx = 216 #Image dimensions
imgy = 384
image = Image.new("HSV", (imgx, imgy))

xa = -1.0
xb =  1.2
ya = -1.8 # Domain of graph, scaled to dimensions
yb =  1.8

maxIt = 30 # max iterations allowed
eps = 0.05 # max error allowed

fps = 60.0  # Frames per second
frames = int(math.ceil(fps*len(song) / 1000.0)) #total frames to be rendered
Sstep = sampleSize/frames   #Step size to synchronize audio-levels with frames

# print(multiplicative(samples, sampleSize/(len(song) / 1000.0), 1, 0.5))


# Create a smaller array with just the audio levels we'll be referencing,
vols = []
maxVol = 0
_temp = 0

while _temp < sampleSize: #Float step isn't allowed in for-loop   
    vols.append(abs(samples[int(_temp)]))
    _temp += Sstep
del _temp
# maxVol = (maxVol+song.max)/2

N = 40
cumsum, moving_aves = [0], []

for i, x in enumerate(vols, 1):
    cumsum.append(cumsum[i-1] + x)
    if i>=N:
        moving_ave = (cumsum[i] - cumsum[i-N])/N
        #can do stuff with moving_ave here
        moving_aves.append(moving_ave)

while (len(moving_aves) < len(vols)):
    moving_aves.append(moving_aves[-1])

vols = moving_aves
maxVol = max(vols)

del cumsum, moving_aves, N, Sstep

def render(start, stop, jobID,q):
    loud = vols[start]/maxVol
    halfy = int(imgy/2)
    for frame in range(start,stop):
        if os.path.exists(folder+"/%04d.png" % frame):
            continue
        q[jobID-1] = ("{}: {}/{}".format(jobID,frame-start,stop-start))

        _i =(0.5*math.sin(frame*math.pi/frames))
        
        # if loud < (vols[frame]/maxVol):
        loud = (vols[frame]/maxVol)**0.5
        #loud = vols[frame]/maxVol
        # else:
            # loud = (loud + ((vols[frame])/maxVol)**0.5)/2.0

        for y in range(halfy):
            zy = y * (yb - ya) / (imgy - 1) + ya
            for x in range(imgx):
                zx = x * (xb - xa) / (imgx - 1) + xa
                z=complex(zx,zy)
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
                
                shadow = float(i)/float(maxIt) * (255*frame/frames)
                
                hue = ((1-shadow**(1+loud))*255) 
                sat = loud*255
                lum = 255*shadow**(3-(-2*loud))

                col = (int(hue), int(sat), int(lum)) 
                image.putpixel((x, y), col)
                image.putpixel((x, imgy-y-1), col)
            
        image.transpose(Image.ROTATE_270).convert("RGB").save(folder+"/%04d.png" % frame, "PNG")
        # sample += Sstep
        # _i+=Mstep
    q[jobID-1] = "{0}:{1}done{1}".format(jobID," "*len(str(stop)))
    return "\nDone."

if __name__ == '__main__':
    cores = cpu_count()*6
    pool = Pool(processes=cores) 
    q = Manager().list(['']*cores)
    print(frames,"frames over",cores,"cores;",imgx*imgy*frames,"total pixels.")
    _time = time()
    res = None
    for job in range(cores):
        start = math.floor(job*frames/cores)
        stop = math.ceil((job+1)*frames/cores)
        res = pool.apply_async(render, (start,stop,job+1,q,))
    pool.close()
    while not res.ready():
        print(" | ".join(q),end="\r",flush=True)
        sleep(10)
    print(res.get())
    pool.join()
    pool.terminate()    
    image.convert("RGB").save(folder+"/_0.tiff", "PNG")
    m, s = divmod(time()-_time, 60)
    h, m = divmod(m, 60)
    print("Job took %d:%02d:%02d to complete" % (h, m, s))
    

