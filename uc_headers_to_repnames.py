#!/usr/bin/python
# Aaron Saunders | ams@bio.aau.dk


import sys
import re

args = sys.argv[1:]
fastafilename = args[0]
ucfilename = args[1]

with open(ucfilename, 'r') as fh:
    clusters = [ line for line in fh if line.startswith('S') ]

ucmap = { }
for line in clusters:
    data = line.rstrip().split('\t')
    clusternumber, clustername = data[1], data[8]
    ucmap[clusternumber] = clustername

print ucmap

fastafile = open(fastafilename, 'r')
stub, dot, ext = fastafilename.rpartition('.')
ucheader_pattern = re.compile(r'>Cluster(\d+)')

count = 0
with open(stub + 'reps.fa', 'w') as outfile:
    for line in fastafile:
        mobj = ucheader_pattern.search(line)
        if mobj:
            clusternumber = mobj.group(1)
            line = '>{}\n'.format(ucmap[clusternumber])
            count += 1
        outfile.write(line)

print 'converted {} headers'.format(count)

