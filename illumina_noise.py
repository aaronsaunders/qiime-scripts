#!/usr/bin/env python

import  os, sys, re 
import commands
from os.path import basename
from Bio import SeqIO
from Bio.SeqIO.QualityIO import FastqGeneralIterator
from optparse import OptionParser
import gzip

"""
A Python program to do some statistics on input sequence file. 
The first version aims to support Fastq files. 
"""


def make_hash_table(inFH):   
    dictUniqSeq = {}
    headers = {}
    intTotalCount = 0

    for title, seq, qual in FastqGeneralIterator(inFH) :
        seq.strip()
        if dictUniqSeq.has_key(seq) :
            dictUniqSeq[seq] += 1
            headers[seq].append(title)
        else :
            dictUniqSeq[seq] = 1
            headers[seq] = [title]
        intTotalCount += 1

    return dictUniqSeq, intTotalCount, headers

def filter_fastq_by_coverage(inFH, filteredFH, keep_reads):
    i = 0
    for title, seq, qual in FastqGeneralIterator(inFH):
        if i < 10:
            print seq
        if seq in keep_reads:
            line = '>%s\n%s+%s\n' % (title, seq, qual)
            filteredFH.write(line)
        i += 1

    inFH.close()
    filteredFH.close()

    return 

def main( filein, outpath, cutoff, inFileName ):

    print 'Working on file: ', filein
    try :  
        inFH = gzip.open(filein, "rb")
    except IOError :
        print "Could not open %s" % filein
        sys.exit()
    try :
        uniquefilename = os.path.join(outpath, inFileName[:-9] + '.unique')
        outFH = open(uniquefilename, "w")
    except IOError :
        print "Could not open %s for writing" % uniquefilename
    try :
        statfilename = os.path.join(outpath, inFileName[:-9] + '_stat.txt')
        outSTATFH = open(statfilename, "w")
    except IOError :
        print "Could not open %s for writing" % statfilename


    dictUniqSeq, intTotalCount, headers  = make_hash_table(inFH)

    sorted_keys = sorted(dictUniqSeq, key=dictUniqSeq.get, 
                                             reverse=True)

    over_cutoff_seqs = []
    over_cutoff_totalcount = 0

    for s in sorted_keys :
        count = dictUniqSeq[s]
        if count >= cutoff :
            over_cutoff_seqs.append(s)
            over_cutoff_totalcount += count
            outFH.write("%s\n" % s )
            outSTATFH.write('%s\t%s\n' % (
                    len(over_cutoff_seqs), dictUniqSeq[s] ))

    print 'Total reads: %i' %  intTotalCount
    print 'Unique reads: %i' % len(dictUniqSeq)
    print 'cutoff: %i' % cutoff
    print 'unique over cutoff: %i' % (len(over_cutoff_seqs))
    print 'count over cutoff: %i' % over_cutoff_totalcount
    print 'percent reads over cutoff: %i' % (
        over_cutoff_totalcount / float(intTotalCount) * 100)

    inFH.close()
    outFH.close()
    outSTATFH.close()
    
    outfilename = '{0}_uniq{1}fasta.gz'.format(inFileName[:-9], cutoff)
    outfilename = os.path.join(outpath, outfilename)
    outfile = gzip.open(outfilename, 'wb')
    for seq in over_cutoff_seqs:
        for header in headers[seq]:
            outfile.write('%s\n%s\n' % (header, seq) )
    outfile.close()

if __name__ == "__main__":

    parser = OptionParser(usage="usage: type %prog -h for more information")
    parser.add_option("-i", "--input",
                     dest="input",
                     help="Input sequence file"
                     )
    parser.add_option("-o", "--output",
                     dest="output",
                     help="File to output sequences after assembling.\
                           Default will be sub_INPUT",
                     )
    parser.add_option("-c", "--cutoff",
                     dest="cutoff",
                     type='int',
                     help="Cutoff value for lowest unique seq abundance",
                     default=1
                     )
    (options, args) = parser.parse_args()
    
    if len(sys.argv) <= 1 :
        parser.print_help()
        exit(0)

    # initialise parameters
    filein = options.input
    outpath = options.output
    cutoff = options.cutoff
    inFileName = basename(filein)
    main( filein, outpath, cutoff, inFileName ) 
