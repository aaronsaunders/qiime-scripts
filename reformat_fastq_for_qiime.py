#!/usr/bin/python

from Bio import SeqIO
from Bio.SeqIO.QualityIO import FastqGeneralIterator
import os.path
import sys

args = sys.argv
fastqfilename = args[1]
outfilename = args[2]
print 'running ' + args[0]
print 'infile: ' + fastqfilename
print 'convert outfile:' + outfilename

count = 0
written = 0

with open(fastqfilename, 'r') as fastqfile:
    outfile = open(outfilename, 'w')
    sample = 'AMPA067'
    # TODO should be scripted from a parameters file in future based on 
    # (cellID, lane number and barcode seq)
    while True:
        count  += 1
        header = fastqfile.readline()
        if not header:
            break
        header = header.strip()
        seqid, barcode_string = header.split()
        read, bad_read, skip, barcode = barcode_string.split(':')
        seq = fastqfile.readline()
        fastqfile.readline()
        fastqfile.readline()
        id = '>{sample}_{count} {seqid}:{read} orig_bc={barcode} new_bc= {barcode} bc_diffs=0\n'.format( \
            sample=sample, seqid=seqid[1:], read=read, barcode=barcode, count=count)
        if bad_read == 'N':
            outfile.write(id + seq)
            written += 1

    print
    outfile.close()
    print 'reformatted {0} of {1} sequences'.format(written, count)
    print 'script DONE!'

