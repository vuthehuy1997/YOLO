import darknet as dn
import os
import random
from PIL import Image, ImageFont, ImageDraw, ImageEnhance

# draw box for all of object that been returned from result
def all_box(draw, objects):
    obs = {}
    for o in objects:
        print (o)
        if o[0] in obs:
            color = obs[o[0]]
        else:
            color = (random.randrange(50,255),random.randrange(50,255),random.randrange(50,255))
            obs[o[0]] = color
        print(color)
        box(draw, o,color)

# draw box for 1 object 
def box(draw, object_detect, color):
    print (object_detect[2][0],object_detect[2][1],object_detect[2][2],object_detect[2][3])
    width = object_detect[2][2]
    heigh = object_detect[2][3]
    x = object_detect[2][0] - width/2
    y = object_detect[2][1] - heigh/2

    rectangle_box(draw, x,y,width,heigh,color)
    text_box(draw, object_detect[0],x, y,color)

# draw rectangle for box
def rectangle_box(draw, x,y,width,heigh, color):
    print("color in rectangle: ",color)
    draw.rectangle(((x, y), (x + width, y + heigh)), outline=color, width=3)

# draw text for box
def text_box(draw, text ,x, y, color):
    font=ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 28, encoding="unic")
    text_size = font.getsize(text)  
    width = text_size[0]+5
    heigh = text_size[1]+5
    
    draw.rectangle(((x, y-heigh), (x+width, y)), fill=color, width=3)
    draw.text((x+2, y+2-heigh), text, font=font, fill='black', width = 3)

# main function to draw box for detected object
def write_detect(net, meta, path, filename):
    
    r = dn.detect_app(net,meta,os.path.join(path, filename))
    print(r)
    print("detected")
    source_img = Image.open(os.path.join(path, filename))
    draw = ImageDraw.Draw(source_img)
    all_box(draw, r)
    output_filename = 'out_'+filename
    print(output_filename)
    os.path.join(path, 'out_'+filename)
    source_img.save(os.path.join(path, output_filename))
    return output_filename

if __name__ == "__main__":
    filename = 'dog.jpg'
    net,meta = dn.load_app()
    r = dn.detect_app(net,meta,filename)
    print(r)
    source_img = Image.open(os.path.join('python/static', filename))

    draw = ImageDraw.Draw(source_img)
    all_box(r)
    source_img.save('python/static/out_dog.jpg')

 
