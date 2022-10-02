import math


f = open("table.txt", "w")
prefix = "4 8 "
suffix = "e"
f.write('{| class="fandom-table" style="width: 100%"\n')
length = 131
rows = math.ceil(length/4)
for i in range(rows):
    for j in range(4):
        if 4*i+j <= length:
            f.write(f'| style="width: 25%" |[[File:{prefix}{4*i+j}{suffix}.jpg|center|frameless|200x200px]]\n')
        else:
            f.write('|\n')
    f.write('|-\n')
f.write('|}\n')
f.close()
