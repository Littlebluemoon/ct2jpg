from PIL import Image, ImageDraw, ImageFont
import os


text = "Area184"
diff = "Easy 6"
dir = os.getcwd() + "\\results"
for filename in os.listdir(dir):
    f = os.path.join(dir, filename)
    num = os.path.splitext(filename)
    page = Image.open(f)
    draw = ImageDraw.Draw(page)
    font = ImageFont.truetype(f"{os.getcwd()}\\Rajdhani-SemiBold.ttf", 60)
    draw.text((80, 2540), text, fill='black', font=font, align='left')
    draw.text((3280, 2540), diff, fill='black', font=font, align='left')
    print(f"Title for page {num[0]} done")
    page.save(f)
