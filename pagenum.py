from PIL import Image, ImageDraw, ImageFont
import os


dir = os.getcwd() + "\\results"
for filename in os.listdir(dir):
    f = os.path.join(dir, filename)
    num = os.path.splitext(filename)
    page = Image.open(f)
    draw = ImageDraw.Draw(page)
    font = ImageFont.truetype(f"{os.getcwd()}\\Rajdhani-SemiBold.ttf", 250)
    text = num[0]
    draw.text((89, 4), text, fill='black', font=font, align='left')
    print(f"Page num for page {num[0]} done")
    page.save(f)
