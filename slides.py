from PIL import Image, ImageDraw, ImageFont
from decimal import Decimal
import csv
import time
import os, shutil

minH = int(440)
maxH = int(2360)
minW = int(280)
maxW = int(3160)


# center of a tick
def center(tick, x, mode=1):
    if mode == 1:
        # down
        noteY = int(minH + (2 * (int(tick) % 960)))
        noteX = int(Decimal(minW + (maxW - minW) * Decimal(x)))
    else:
        # up
        noteY = int(maxH - (2 * (int(tick) % 960)))
        noteX = int(Decimal(minW + (maxW - minW) * Decimal(x)))
    return (noteX, noteY)


t1 = time.time()
point1 = ()
drags = []
notes = []
with open("notes.csv", encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        notes.append(row)
with open("linklist.csv", encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        drags.append(row)
# purge the directory
folder = os.getcwd() + "\\results"
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))
# create {maxPage} placeholder images
maxPage = int(notes[len(notes)-1][5])
print("Creating placeholder pages ...",end='')
src = str(f"{os.getcwd()}\\graphics\\pages\\arena.png")
for i in range (maxPage+1):
    tgt = str(f"{os.getcwd()}\\results\\{i}.jpg")
    shutil.copy(src, tgt)
print(" done")
# seek for pages inside each drag commands, then draw
for row in drags:
    point1 = point2 = ()
    for i in range (len(row)-1, -1, -1):
        # get page #
        pageNo = int(notes[int(row[i])][5])
        # start editing on that page
        pages = Image.open(f"{os.getcwd()}\\results\\{pageNo}.jpg")
        # get coords to draw line
        page_ = ImageDraw.Draw(pages)
        point2 = point1
        if pageNo % 2 == 1:
            point1 = center(notes[int(row[i])][1], notes[int(row[i])][2], 1)
        else:
            point1 = center(notes[int(row[i])][1], notes[int(row[i])][2], -1)
        print(f"Connected drags in page {pageNo}, from {point1} to {point2}")
        if not point2:
            pass
        else:
            page_.line([point1, point2], fill='black', width=20)
        pages.save(f"{os.getcwd()}\\results\\{pageNo}.jpg", compression_level=3)
print(f"Time taken: {time.time()-t1}s")
