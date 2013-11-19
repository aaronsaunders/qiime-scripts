#!/usr/bin/env python
 
"""
Usage: seqIDs_from_otus.py [id_list] [seqs_otus.txt] [seqs.fna] [outfile.fna]

takes a list of OTU IDs and the qiime otu mapping file

returns a list of seqnames to file (filename last argument)

Copyright (C) 2013 Aaron Saunders ams@bio.aau.dk

"""
import sys
from Bio import SeqIO

args = sys.argv[1:]

if len(args) == 2:
    idfname = args[0]
    otufname = args[1]
    seqsfname = args[2]
    outfname = args[3]
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
            otus = line.split('\t')[1:]
            for otu in otus:
                seqnames.append(otu)
            
fasta_dict = SeqIO.index(seqsfname, "fasta")

recstokeep = [ fasta_dict[seqid] for seqid in seqnames ]

with open(outfname, 'w') as outfh:
    SeqIO.write(recstokeep, outfh, "fasta")

handle = open(outfname, 'w')
for record in recstokeep:
    handle.write(">%s\n%s\n" % (record.description, record.seq))
handle.close()

