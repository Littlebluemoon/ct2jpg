import decimal
from decimal import Decimal
import math

def toTick(t, size):
    return math.floor(Decimal(t / size * 960))

def pageNum(t, size=960):
    return math.floor(t / size)

f = open("chart.txt", "r")
f.readline()
# bpm
bpm = Decimal(str(f.readline())[4:]) / 2
# shift
shift = Decimal(str(f.readline())[10:])
# size
size = Decimal(str(f.readline())[9:])
# notes data
notes = []
rows = []
stop = 0
data = ""
# format: [index, time, x-axis, hold duration, type, page]
# firstly type with be defaulted to 0
while not stop:
    data = f.readline()
    if not data:
        break
    elif data[0] == 'N' and data:
        data = data[5:len(data) - 1]
        rows = data.split('\t')
        rows.append('0')
        rows.append('0')
        notes.append(rows)
    else:
        break
# get drag data
rows = []
drags = []
data = data[5:len(data) - 1]
rows = data.split()
drags.append(rows)
while True:
    data = f.readline()
    if data != '':
        data = data[5:len(data) - 1]
        rows = data.split()
        drags.append(rows)
    else:
        break
# set note types
# 0: click
# 1: hold
# 2: drag
# 3: dragChild
for i in drags:
    for j in range(len(i)):
        if j == 0:
            notes[int(i[int(j)])][4] = '2'
        else:
            notes[int(i[int(j)])][4] = '3'
# holds
for i in notes:
    if Decimal(i[3]) != Decimal('0'):
        i[4] = '1'
# write to file
out = open("notes.csv", "w", encoding='utf-8')
for i in notes:
    i[1] = str(toTick(Decimal(Decimal(i[1]) + shift), size))
    i[3] = str(toTick(Decimal(Decimal(i[3])), size))
    i[5] = str(pageNum(Decimal(i[1])))
    line = ','.join(i)
    out.write(line + '\n')
links = open("linklist.csv", "w", encoding='utf-8')
if len(drags) > 1:
    drags.sort(key=lambda x: int(x[0]))
for i in drags:
    data1 = ','.join(i)
    links.write(data1 + '\n')
out.close()
links.close()
