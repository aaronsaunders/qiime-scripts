#!/usr/bin/python
# by Aaron (ams@bio.aau.dk)


import sys
import os
import subprocess

"""
preprocess_illumina.py [in directory] [out directory] [unique cutoff]
"""

#print start time
print sys.argv[0]
# print version

inpath = sys.argv[1]
outpath = sys.argv[2]
cutoff = int(sys.argv[3])
print 'inpath: %s' % inpath 
print 'outpath: %s' % outpath  
print 'cutoff: %i' % cutoff

contig_dir = os.path.join(outpath, 'contigs')
if not os.path.isdir(contig_dir):
    os.mkdir(contig_dir)
cmd = 'python ~/scr/qiime-scripts/assemble_batch_pandaseq.py {0} {1}'.format(
    inpath, contig_dir)
print cmd
#subprocess.call(cmd, shell=True)
print 'assembled'

unique_dir = os.path.join(outpath, 'unique')
if not os.path.isdir(unique_dir):
    os.mkdir(unique_dir)
contigs = [ fname for fname in os.listdir(contig_dir)
            if fname.endswith('.fastq.gz')]
for contig in contigs:
    contigpath = os.path.join(contig_dir, contig)
    cmd = 'python ~/scr/qiime-scripts/batch_unique.py -i {0} -o {1} -c {2}'.format(contigpath, unique_dir, cutoff)
    print cmd
    subprocess.call(cmd, shell=True)


qiime_dir = os.path.join(outpath, 'qiime')
if not os.path.isdir(qiime_dir):
    os.mkdir(qiime_dir)
cmd = 'python ~/scr/qiime-scripts/reformat_fasta_for_qiime.py {0} {1}'.format(
                                   unique_dir, qiime_dir)
print cmd
subprocess.call(cmd, shell=True)

cmd =  'cat ./qiime/*.fasta > seqs.fna'
subprocess.call(cmd, shell=True)
print cmd
  
