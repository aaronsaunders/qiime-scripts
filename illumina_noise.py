#!/usr/bin/env python

from __future__ import division
__author__ = "aaron modified from Vang Quy Le"
__copyright__ = "Copyright 2012"
__credits__ = ["Vang Quy Le"]
__license__ = "GPL"
__version__ = "0.3"
__maintainer__ = "Vang Quy Le"
__email__ = "lqvang79@gmail.com"
__status__ = "Beta2"
import  os, sys, re 
import warnings
import commands
from os.path import basename
from Bio import SeqIO
from Bio.SeqIO.QualityIO import FastqGeneralIterator
from optparse import OptionParser
from numpy import median
import gzip

"""
A Python program to do some statistics on input sequence file. 
The first version aims to support Fastq files. 
"""


script_info = {}
script_info['message'] = 'Do some basic statistics on sequence file '
#script_info['script_description']
#script_info['brief_description']
#script_info['script_description']
#script_info['script_usage']=[]
#script_info['output_description']
#script_info['required_options']
#script_info['optional_options']
script_info['version'] = __version__
print script_info['message']


def make_hash_table(inFH, seqFormat, iStart, iEnd):   
    dictUniqSeq = {}
    intTotalCount = 0
    #print seqFormat
    if seqFormat == 'fastq'.lower() :
        for title, seq, qual in FastqGeneralIterator(inFH) :
        #outFH.write("@%s\n%s\n+\n%s\n" % (title, seq[:trim], 
        #                                         qual[:trim]))
            seq.strip()
            #print seq
            trSeq = seq[iStart:iEnd]
            if dictUniqSeq.has_key(trSeq) :
                dictUniqSeq[trSeq] += 1
            else :
                dictUniqSeq[trSeq] = 1
            intTotalCount += 1
    if seqFormat == 'fasta'.lower() :
        for record in SeqIO.parse(inFH, "fasta") :
            seq = record.seq
            #print seq
            trSeq = seq[iStart:iEnd]
            if dictUniqSeq.has_key(trSeq) :
                dictUniqSeq[trSeq] += 1
            else :
                dictUniqSeq[trSeq] = 1
            intTotalCount += 1
    
    return dictUniqSeq, len(dictUniqSeq), intTotalCount


def main( filein, fileout, fileStat, seqFormat, cutoff, iStart,
         iEnd, inFileName ):

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        print 'Working on file: ', filein
        try :  
            inFH = gzip.open(filein, "rb")
        except IOError :
            print "Could not open %s" % filein
            sys.exit()
        try :
            outFH = open(fileout, "w")
        except IOError :
            print "Could not open %s for writing" % fileout
        try :
            outSTATFH = open(fileStat, "w")
        except IOError :
            print "Could not open %s for writing" % fileStat

        
        dictUniqSeq, intNumUniq, intTotalCount  = make_hash_table(
                                     inFH, seqFormat, iStart, iEnd)

        intMedian = median(dictUniqSeq.values())
        
        sorted_keys = sorted(dictUniqSeq, key=dictUniqSeq.get, 
                                                 reverse=True)
        over_cutoff_tally = 0
        over_cutoff_totalcount = 0
        for s in sorted_keys :
            count = dictUniqSeq[s]
            if count >= cutoff :
                over_cutoff_tally += 1
                over_cutoff_totalcount += count
                outFH.write (">seq_%s_%s\n%s\n" % (
                             over_cutoff_tally , dictUniqSeq[s], s ))
                outSTATFH.write('%s\t%s\n' % (
                             over_cutoff_tally, dictUniqSeq[s] ))
        over_cutoff_percent = ( over_cutoff_totalcount / intTotalCount) * 100

        print 'TotalCount: %i' %  intTotalCount
        print 'UniqueCount: %i' % intNumUniq
        print 'over cutoff: %i (cutoff: %i)' % (over_cutoff_tally, cutoff)
        print 'count over cutoff: %i' % over_cutoff_totalcount
        print 'percent over cutoff: %.2f' % over_cutoff_percent


if __name__ == "__main__":

    parser = OptionParser(usage="usage: type %prog -h for more information",
                          version=script_info['version'])
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
    parser.add_option("-f", "--format",
                     dest="format",
                     help="Input and output sequence format. \
                          Currently support 'fasta' and 'fastq'. \
                          Default will be fastq",
                     default='fastq'
                     )
    parser.add_option("-s", "--stat",
                     dest="stat",
                     help="File to output statistic infor. \
                           Default will be stat_INPUT",
                     ) 
    parser.add_option("-b", "--start",
                     dest="start",
                     help="Start sequence index to do statistic on, \
                           [default = 0]",
                     type='int',
                     default=0
                     )
    parser.add_option("-e", "--end",
                     dest="end",
                     help="End sequence index to do stat on, [default=100]",
                     type='int',
                     default=100)
    (options, args) = parser.parse_args()
    
    if len(sys.argv) <= 1 :
        parser.print_help()
        exit(0)

    # initialise parameters
    filein = options.input
    fileout = options.output
    fileStat = options.stat
    seqFormat = options.format
    cutoff = options.cutoff
    iStart = options.start
    iEnd = options.end
    inFileName = basename(filein)
    if fileout is None :
        fileout = 'sub_' + inFileName 
    if fileStat is None :
        fileStat = 'stat_' + inFileName
    main( filein, fileout, fileStat, seqFormat, cutoff, iStart,
         iEnd, inFileName ) 
