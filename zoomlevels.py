import os, threading, time
from PIL import Image

zoomlevels = 4
threads = os.process_cpu_count() or os.cpu_count() or 4

maxx = 0
minx = 0
maxy = 0
miny = 0
files = []

for f in os.listdir(os.path.normpath(os.path.join(os.getcwd(),"../day"))):
    xy = f.split(".",1)[0]
    try:
        x, y = xy.split(",",1)
    except ValueError:
        continue
    maxx = max(maxx, int(x))
    minx = min(minx, int(x))
    maxy = max(maxy, int(y))
    miny = min(miny, int(y))
    files.append(f)
imagedim = (abs(maxx-minx+1)*512,abs(maxy-miny+1)*512)

# the multithreading is definitely not just for fun ;3
threadpool = [None] * threads
threadqueue = []

def processgroup(zg,z,n):
    img = Image.new("RGBA",(512,512))
    for segpath, sx, sy in zg:
        try:
            segment = Image.open(segpath)
        except Exception as e:
            print(e)
            continue
        img.paste(segment.resize([512>>z]*2,Image.BICUBIC),(sx*(512>>z),sy*(512>>z)))
        segment.close()
    img.save(os.path.join(os.getcwd(),str(zoomlevels-(z+1)),n))
    print("processed {0}/{1}".format(z,n))

print(minx, miny, maxx, maxy, imagedim)
for z in range(zoomlevels):
    if not os.path.exists(os.path.join(os.getcwd(),str(zoomlevels-(z+1)))):
        os.mkdir(os.path.join(os.getcwd(),str(zoomlevels-(z+1))))
    zoomgroups = {}
    for f in files:
        print(z,f)
        x, y = f.split(".",1)[0].split(",",1)
        try:
            x = int(x)
            y = int(y)
        except ValueError:
            continue
        gx = x>>z
        gy = y>>z
        sx = x%(1<<z)
        sy = y%(1<<z)
        if not (gx,gy) in zoomgroups:
            zoomgroups[(gx,gy)] = []
        zoomgroups[(gx,gy)].append((os.path.normpath(os.path.join(os.getcwd(),"../day",f)),sx,sy))

    for zoomgroup in zoomgroups:
        threadqueue.append(threading.Thread(target=processgroup,args=(zoomgroups[zoomgroup],z,"{0},{1}.png".format(*zoomgroup))))

try:
    while len(threadqueue):
        for i,thread in enumerate(threadpool):
            if thread == None or not thread.is_alive():
                if len(threadqueue):
                    thread = threadqueue.pop(0)
                    thread.start()
                    threadpool[i] = thread
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

for thread in threadpool:
    if thread != None and thread.is_alive():
        thread.join()
