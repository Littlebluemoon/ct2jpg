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
folder = os.getcwd() + "\\results"
# seek for pages inside each drag commands, then draw
for row in drags:
    point1 = point2 = ()
    for i in range (len(row)-1, -1, -1):
        # get page #
        pageNo = int(notes[int(row[i])][5])
        if pageNo == 0:
            pass
        else:
            # start editing on that page
            pages = Image.open(f"{os.getcwd()}\\results\\{pageNo-1}.jpg")
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
                page_.line([point1, point2], fill=(127,127,127), width=20)
            pages.save(f"{os.getcwd()}\\results\\{pageNo-1}.jpg")
print(f"Time taken: {time.time()-t1}s")
