from PIL import Image, ImageDraw, ImageFont
import os


prefix = "4 7 "
suffix = "e"
dir = os.getcwd() + "\\results"
for filename in os.listdir(dir):
    f = os.path.join(dir, filename)
    no_ext = os.path.splitext(filename)
    text = prefix+no_ext[0]+suffix+".jpg"
    new = os.path.join(dir, text)
    os.rename(f, new)

