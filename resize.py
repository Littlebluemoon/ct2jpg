from PIL import Image
import os


dir = os.getcwd() + "\\results"
for filename in os.listdir(dir):
    f = os.path.join(dir, filename)
    num = os.path.splitext(filename)
    page = Image.open(f)
    page = page.resize((1780, 1335))
    print(f"Page {num[0]} resized to {page.size}")
    page.save(f)
