from PIL import Image
import os
os.makedirs("output", exist_ok=True)
os.makedirs("textures/RGB_cube", exist_ok=True)
WIDTH = 720
HEIGHT = 720
imgs = []
for _ in range(6):
    imgs.append(Image.new("RGB",(WIDTH,HEIGHT)))

pixels = imgs[0].load()
for y in range(HEIGHT):
    for x in range(WIDTH):
        pixels[x,y] = (int(x/(WIDTH-1)*255),int(y/(WIDTH-1)*255),0)

pixels = imgs[1].load()
for y in range(HEIGHT):
    for x in range(WIDTH):
        pixels[x,y] = (int(x/(WIDTH-1)*255),0,int(y/(WIDTH-1)*255))
        
pixels = imgs[2].load()
for y in range(HEIGHT):
    for x in range(WIDTH):
        pixels[x,y] = (0,int(x/(WIDTH-1)*255),int(y/(WIDTH-1)*255))

pixels = imgs[3].load()
for y in range(HEIGHT):
    for x in range(WIDTH):
        pixels[x,y] = (int(x/(WIDTH-1)*255),int(y/(WIDTH-1)*255),255)

pixels = imgs[4].load()
for y in range(HEIGHT):
    for x in range(WIDTH):
        pixels[x,y] = (int(x/(WIDTH-1)*255),255,int(y/(WIDTH-1)*255))
        
pixels = imgs[5].load()
for y in range(HEIGHT):
    for x in range(WIDTH):
        pixels[x,y] = (255,int(x/(WIDTH-1)*255),int(y/(WIDTH-1)*255))

for i in range(6):
    imgs[i].save(f"textures/RGB_cube/cubeside{i}.png")

Image.new("RGB", (WIDTH,HEIGHT),(255,255,255)).save(f"textures/white_t.png")