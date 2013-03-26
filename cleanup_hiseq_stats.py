#!/usr/bin/python
# ams@bio.aau.dk	

import sys
import os.path

fpath = sys.argv[1]
fname = os.path.split(fpath)[1]
project = sys.argv[2]
projectline = 'Project: ' + project

with open(fpath, 'r') as fh:
    lines =  [ line.strip() for line in fh.readlines() ] 

# sort out lines for the project
startln = 0
for ln, line in enumerate(lines):
    if line.startswith(projectline):
        startln = ln + 1
        print line
        continue
    if startln and line.startswith('Project: '):
        stopln = ln
        break

lines = [ line.strip().split('\t') for line in lines[startln:stopln] ]

# reformat lines for each sample
output = []
ln= 0
while ln < len(lines):
    amplib = lines[ln][0].strip(':')
    ln += 1
    if lines[ln][0].startswith('ERROR'):
        ln += 1    
    R1 = lines[ln][0].strip(':')
    depth = lines[ln][2]
    ln += 1
    if lines[ln][0].startswith('ERROR'):
        ln += 1
    R2 = lines[ln][0].strip(':')
    ln += 1
    newline = '{0}\t{1}\t{2}\t{3}\n'.format(amplib, depth, R1, R2)
    output.append(newline)

fnamestem, ext = os.path.splitext(fname)
outfname = fnamestem + '_' + project + '.txt'
with open(outfname, 'w') as fh:
    fh.writelines(output)	
	

