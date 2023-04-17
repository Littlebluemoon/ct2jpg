## CT2jpg - Cytus I Chart to .jpg converter
## Overview
This is a small program that will convert chart files in the rhythm game, Cytus I, into static pages in .jpg for reference while studying the patterns of a specific chart.
## Requirements
Python 3.x, with Pillow installed
## Files
### Text Files
 - **chart.txt** - Your chart file. You can get the files from the game's obb by using UABE or any similar tool.
 - **notes.csv** - A list of notes including timestamps and note type
 - **linklist.csv** - A list of drags in the chart, starting with a drag head followed by drag child(s)
 ### Source Files
 - **fork.py** - Get data from the chart file and push it all into **notes.csv** and **linklist.csv**
 - **slides.py**, **slides_shadow.py** - Draw draglines and shadow draglines
 - **toimage_shadow.py** - Put shadow notes
 - **toimage.py** - Put notes and gridlines
 - **pagenum.py** - Put page numbers
 - **title.py** - Put song name and difficulty
 - **execute.py** - Run the program
 ### Misc
 - **graphics** - Contains note skins and playfield
 - **results** - Resulting images are put here
 - **rename.py** - Batch rename all files, used for my wiki only
 - **wiki.py** - Create fandom-table off a template, used for my wiki only
 - **table.txt** - Resulting file from **wiki.py**, used for my wiki only
## Usage
Run **execute.py**, or these, in order:
1. **fork.py**
2. **slides.py**, **slides_shadow.py** (regardless of order)
3. **toimage_shadow.py**
4. **toimage.py**
5. **pagenum.py**, **title.py** (regardless of order)
6. (Optional) **rename.py**, **resize.py**. These file were added by default in **execute.py** for my works.
## The magic behind
### The chart files
The chart files always follow this pattern:
- they start with this message
```
VERSION 2
BPM X
PAGE_SHIFT Y
PAGE_SIZE Z
```
where 
+ X is the BPM of the song multipled by 2
+ Y is the duration in seconds, that the chart was made to start later, compared to its beginning
+ Z is the duration of each chart page in seconds, conveniently ```240/X```
+ for example, if a chart has these messages in the beginning
```
VERSION 2
BPM 160.000000
PAGE_SHIFT 0.750000
PAGE_SIZE 1.500000
```
then the chart's BPM is 80, each page of the chart is 1.5s in length, and right when the chart starts you will find its scanline at the exact middle of the screen, since ```0.75/1.5=0.5```.
I dunno why the game creators decided to use double the BPM to reflect the chart's BPM though, could be some bug-turned-feature shenanigans.
+ then it is followed by
```
NOTE	0	X0	Y0	Z0
NOTE	1	X1	Y1	Z1
...
```
+ NOTE declare a note's existence. It is followed by 4 tab-separated number, plus one tab right after itself. The first one is its id, starting from 0. ```Xn``` is the timestamp, ```Yn``` is its x-position, ```Zn``` is its hold duration, measured in seconds. If ```Zn == 0.000000```, then the note is a click, or a drag note, otherwise it is a hold note.
+ Then if the chart happens to have any drag notes, these message follows
```
LINK X0 X1 X2 X3 ...
LINK Y0 Y1 Y2 Y3 ...
...
```
+ LINK declares a string of drag notes. It is then followed by some space-separated numbers denoting the id of notes within it. The first one will be the drag head, the other will be its drag childs.
