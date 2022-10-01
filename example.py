from PIL import Image, ImageDraw


img = Image.new('RGB', (500, 300), (128, 128, 128))
draw = ImageDraw.Draw(img)
draw.line((0, 0, 200, 200), fill=(255, 0, 0), width=10)
img.show()
img.save("G:\\draw.png")
