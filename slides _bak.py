from PIL import Image, ImageDraw
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
pageCnt = 0
pageMax = int(notes[len(notes)-1][5])
currPg = []
cursor = 0
for page in range(0, pageMax + 1):
    point2 = ()
    point1 = ()
    currPg = []
    while True:
        if int(notes[len(notes)-1][0]) >= cursor:
            if int(notes[cursor][5]) == page:
                currPg.append(notes[cursor])
                cursor += 1
            else:
                break
        else:
            break
    i = 0
    while i < len(currPg):
        try:
            if int(currPg[i][4]) == 2 or int(currPg[i][4]) == 3:
                pass
            else:
                # print(f"delete {currPg[i]}")
                currPg.remove(currPg[i])
                i = int(-1)
        except IndexError:
            pass
        i += 1
    print(currPg)
    pages = Image.open("G:\\ct2png\\graphics\\pages\\arena.png")
    for note in currPg:
        if page % 2 == 0:
            point2 = point1
            point1 = center(note[1], note[2], -1)
            print(point1, point2)
            page_ = ImageDraw.Draw(pages)
            if not point2:
                print("x")
                page_.line([point1, point1], fill="black", width=20)
            else:
                page_.line([point1, point2], fill="black", width=20)
        else:
            point2 = point1
            point1 = center(note[1], note[2], 1)
            print(point1, point2)
            page_ = ImageDraw.Draw(pages)
            if not point2:
                print("x")
                page_.line([point1, point1], fill="black", width=20)
            else:
                page_.line([point1, point2], fill="black", width=20)

    pages.save(f"G:\\ct2png\\results\\{page}.png") 
        
