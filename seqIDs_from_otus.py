#!/usr/bin/env python
 
"""
Usage: seqIDs_from_otus.py [id_list] [seqs_otus.txt]

returns a list of seqnames to stdout

Copyright (C) 2013 Aaron Saunders ams@bio.aau.dk

"""
import sys

args = sys.argv[1:]

if len(args) == 2:
    idfname = args[0]
    otufname = args[1]
else:
    sys.exit(__doc__)

    
with open(idfname, 'r') as fh:
    otuids = [ id.strip() for id in fh.readlines() ]

seqnames = []
with open(otufname, 'r') as fh:
    for line in fh.readlines():
        line = line.strip()
        otuid = line.split('\t')[0]
        if otuid in otuids:
            seqnames.extend( line.split('\t')[1:] )
            
result = '\n'.join(seqnames)

sys.stdout.write(result)    




