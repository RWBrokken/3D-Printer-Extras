#!/usr/bin/python
# File which was created after looking over other sort and append scripts, modified for gcode alterations
# Although can be used as an example to build from, this was intended to reduce and split the steps in a single
# gcode line to Klipper firmware that exceeded the max number of steps the microcontroller could process
# Coded by Richard B. May 2019, last modified Oct 2019


import os
from os import path
import sys
import fileinput
import re

def getFcount(lineidx):
    if lineidx==fcount:
        return round(float((lineidx-1)/(fcount*1.0)),2)
    else:
        return (round(float((lineidx-1)/(fcount*1.0)),3)-0.001)

def update_progress(job_title, progress):
    length = 25 # modify this to change the length
    block = int(round(length*progress))
    msg = "\r{0}: [{1}] {2}%".format(job_title, "#"*block + "-"*(length-block), round(progress*100, 2))
    if progress >= 1: msg += " DONE\r\n"
    sys.stdout.write(msg)
    # sys.stdout.flush()

# argument check
if len(sys.argv) - 1 < 2:
    print("\n")
    print("\tERROR:  not enough arguments given.")
    print("\t\tProvide an input and output file!")
    print("\n")
    exit(1)

# output file check
if path.exists(sys.argv[2]):
    try:
        if sys.argv[3] == '!':
            print('\n\tOutput file exists but override active')
    except:
        print('\n\t'+sys.argv[2]+' exists!!    Exiting....')
        print('\n')
        exit(2)

# get total lines in input file
fcount = 0
thefile = open(sys.argv[1], 'rb')
while 1:
    buffer = thefile.read(8192*1024)
    if not buffer: break
    fcount += buffer.count('\n')
thefile.close(  )
print('\n\t'+sys.argv[1]+' contains '+str(fcount)+' lines\n')

# begin changes and transcribing
with open(sys.argv[1],'r') as rf:
    print ("\tOpening "+sys.argv[1])
    with open(sys.argv[2],'w') as wf:

        coords = []
        count = 0
        fixes = 0
        lineidx = 1

        for line in rf:
            if lineidx == 4:
                wf.write('\n;\n')
                wf.write(';;    Modified for Klipper RA6+ 2-in-1     ')
                wf.write('\n;\n')

            if 'E75' in line:
                coords.append([str(stgin) for stgin in line.strip().split(' ')])
                out = "G1 "
                out2 = "G1 "
                for word in coords[count]:
                    if 'X' in word:
                        out = out + word + " "
                    if 'Y' in word:
                        out = out + word + " "
                    if 'E' in word:
                        out2 = out2 + word + " "
                    if 'F' in word:
                        out = out + word
                        out2 = out2 + word
                wf.write(out)
                wf.write("\n")
                wf.write(out2)
                wf.write("\n")
                count=count+1
                fixes=fixes+1

            else:
                wf.write(line)

            update_progress("Processing",getFcount(lineidx))
            lineidx = lineidx + 1

        print("\n\tNum:fixes = " + str(fixes))
        print("\tWritten to " + sys.argv[2] + "\n")
