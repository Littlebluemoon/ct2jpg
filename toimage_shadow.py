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


# add click notes
# start of playfield h=440 w=280
# end of playfield h=2360 w=3160
def addClick(tick, x, mode=1) -> (int, int):
    if mode == 1:
        # down
        noteY = int(minH + (2 * (int(tick) % 960)))
        noteX = int(Decimal(minW + (maxW - minW) * Decimal(x)))
    else:
        # up
        noteY = int(maxH - (2 * (int(tick) % 960)))
        noteX = int(Decimal(minW + (maxW - minW) * Decimal(x)))
    #600x600
    return (noteX-300, noteY-300)


# add holds
def addHold(tick, x, mode=1):
    # 690x690
    if mode == 1:
        # down
        headY = int(minH + (2 * (int(tick) % 960)))
        headX = int(Decimal(minW + (maxW - minW) * Decimal(x)))
    else:
        # up
        headY = int(maxH - (2 * (int(tick) % 960)))
        headX = int(Decimal(minW + (maxW - minW) * Decimal(x)))
    return (headX-345, headY-345)

def trackHeight(length):
    if int(length) == 960:
        return Decimal(2040)
    return Decimal(120) + Decimal(int(length) % 960 * 2)


def trackPos(length, tick, x, mode=1):
    if int(length) == 960:
        if mode == -1:
            xCor = int(Decimal(minW + (maxW - minW) * Decimal(x))) - int(104)
            yCor = int(2480) - int(trackHeight(int(length)))
        else:
            xCor = int(Decimal(minW + (maxW - minW) * Decimal(x))) - int(104)
            yCor = int(minH) - int(120)
    else:
        if mode == -1:
            xCor = int(Decimal(minW + (maxW - minW) * Decimal(x))) - int(104)
            yCor = int(2480) - int(trackHeight(int(length))) - int(2 * (int(tick) % 960))
        else:
            xCor = int(Decimal(minW + (maxW - minW) * Decimal(x))) - int(104)
            yCor = int(minH + (2 * (int(tick) % 960))) - int(120)
    return (xCor, yCor)


def addDragHead(tick, x, mode=1):
    if mode == 1:
        # down
        headY = int(minH + (2 * (int(tick) % 960)))
        headX = int(Decimal(minW + (maxW - minW) * Decimal(x)))
    else:
        # up
        headY = int(maxH - (2 * (int(tick) % 960)))
        headX = int(Decimal(minW + (maxW - minW) * Decimal(x)))
    return (headX-300, headY-300)

def addDragChild(tick, x, mode=1):
    if mode == 1:
        # down
        headY = int(minH + (2 * (int(tick) % 960)))
        headX = int(Decimal(minW + (maxW - minW) * Decimal(x)))
    else:
        # up
        headY = int(maxH - (2 * (int(tick) % 960)))
        headX = int(Decimal(minW + (maxW - minW) * Decimal(x)))
    return (headX-108, headY-108)


t1 = time.time()
click_up = Image.open("graphics/notes/noteRed_shadow.png").convert("RGBA")
click_dn = Image.open("graphics/notes/noteGreen_shadow.png").convert("RGBA")
hold = Image.open("graphics/notes/hold_shadow.png").convert("RGBA")
track = Image.open("graphics/notes/holdTrack_shadow.png").convert("RGBA")
head = Image.open("graphics/notes/dragHead_shadow.png").convert("RGBA")
child = Image.open("graphics/notes/dragChild_shadow.png").convert("RGBA")
notes = []
with open("notes.csv", encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        notes.append(row)
pageCnt = 0
pageMax = int(notes[len(notes)-1][5])
currPg = []
cursor = 0
for page in range(pageMax+1):
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
    if page == 0:
        pass
    else:
        pages = Image.open(f"results/{page-1}.jpg").convert("RGBA")
        for j in range(len(currPg)-1, -1, -1):
            if int(currPg[j][4]) == 0:
                if page % 2 == 0:
                    pages.paste(click_up, addClick(currPg[j][1], currPg[j][2], -1), click_up)
                else:
                    pages.paste(click_dn, addClick(currPg[j][1], currPg[j][2], 1), click_dn)
            elif int(currPg[j][4]) == 1:
                if page % 2 == 0:
                    track = Image.open("graphics/notes/holdTrack_shadow.png").convert("RGBA")
                    track = track.rotate(180, expand=True)
                    track = track.resize((208, int(trackHeight(currPg[j][3]))))
                    pages.paste(track, trackPos(currPg[j][3], currPg[j][1], currPg[j][2], -1), track)
                    pages.paste(hold, addHold(currPg[j][1], currPg[j][2], -1), hold)
                else:
                    track = Image.open("graphics/notes/holdTrack_shadow.png").convert("RGBA")
                    track = track.resize((208, int(trackHeight(currPg[j][3]))))
                    pages.paste(track, trackPos(currPg[j][3], currPg[j][1], currPg[j][2], 1), track)
                    pages.paste(hold, addHold(currPg[j][1], currPg[j][2], 1), hold)
            elif int(currPg[j][4]) == 2:
                if page % 2 == 0:
                    pages.paste(head, addDragHead(currPg[j][1], currPg[j][2], -1), head)
                else:
                    pages.paste(head, addDragHead(currPg[j][1], currPg[j][2], 1), head)
            elif int(currPg[j][4]) == 3:
                if page % 2 == 0:
                    pages.paste(child, addDragChild(currPg[j][1], currPg[j][2], -1), child)
                else:
                    pages.paste(child, addDragChild(currPg[j][1], currPg[j][2], 1), child)
        print(f"Processed page {page} / {pageMax}, {cursor} / {notes[len(notes)-1][0]} notes added")
        pages = pages.convert("RGB")
        pages.save(f"results/{page-1}.jpg")
print("Files saved to /results")
print(f"Time taken: {time.time()-t1}s")
