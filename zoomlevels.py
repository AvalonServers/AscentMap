import os
from PIL import Image

zoomlevels = 4

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

print(minx, miny, maxx, maxy, imagedim)

for z in range(zoomlevels):
    if not os.path.exists(os.path.join(os.getcwd(),str(zoomlevels-(z+1)))):
        os.mkdir(os.path.join(os.getcwd(),str(zoomlevels-(z+1))))
    zoomgroups = {}
    for f in files:
        print(z,f)
        try:
            segment = Image.open(os.path.normpath(os.path.join(os.getcwd(),"../day",f)))
        except Exception as e:
            print(e)
            continue
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
            zoomgroups[(gx,gy)] = Image.new("RGBA",(512,512))
        zoomgroups[(gx,gy)].paste(segment.resize([512>>z]*2,Image.BICUBIC),(sx*(512>>z),sy*(512>>z)))
        segment.close()

    for zoomgroup in zoomgroups:
        print("saving {0} {1},{2}.png".format(z,*zoomgroup))
        zoomgroups[zoomgroup].save(os.path.join(os.getcwd(),str(zoomlevels-(z+1)),"{0},{1}.png".format(*zoomgroup)))
