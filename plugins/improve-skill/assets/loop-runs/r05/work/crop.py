import sys
from PIL import Image, ImageDraw
src,out,x0,y0,x1,y1,scale=sys.argv[1],sys.argv[2],*map(int,sys.argv[3:7]),int(sys.argv[7])
im=Image.open(src).convert('RGB').crop((x0,y0,x1,y1))
im=im.resize(((x1-x0)*scale,(y1-y0)*scale),Image.NEAREST)
d=ImageDraw.Draw(im)
step=50
for gx in range(x0-x0%step+step, x1, step):
    px=(gx-x0)*scale; d.line([(px,0),(px,im.height)],fill=(255,0,0),width=1); d.text((px+2,2),str(gx),fill=(255,0,0))
for gy in range(y0-y0%step+step, y1, step):
    py=(gy-y0)*scale; d.line([(0,py),(im.width,py)],fill=(0,160,255),width=1); d.text((2,py+2),str(gy),fill=(0,160,255))
im.save(out); print(out, im.size)
