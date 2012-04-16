#!/usr/bin/python

import sys
import os
import gzip

def qiimeformat_single_fasta(fastafilename, outpath):
    """
    reformats the standard illumina header for qiime.
    """
    try:
        fastafile = gzip.open(fastafilename, 'rb') 
        print 'infile: %s' % fastafilename
    except IOError:
        print 'could not open %s' % fastafilename
        return
    sample = fastafilename.split('_')[0]
    outfilename = sample + '.fna.gz'
    outfilepath = os.path.join(outpath, outfilename)
    try:
        outfile = gzip.open(outfilepath, 'wb')
    except IOError:
        print 'could not open %s' % outfilepath
        return

    print 'outfile: %s' % outfilepath
    count = 0

    for line in fastafile.readlines():
        if line.startswith('>'):
            count  += 1
            read, colon, barcode = line.strip().rpartition(':')
            line = '>{sample}_{count} {read} orig_bc={barcode} \
                    new_bc= {barcode} bc_diffs=0\n'.format(
                                  sample=sample, read=read[1:],
                                  barcode=barcode, count=count)
        outfile.write(line)

    print 'reformatted %i sequences' % count

    fastafile.close()
    outfile.close()

    return 

def main():
    print 'running ' + sys.argv[0]

    inpath = sys.argv[1]
    outpath = sys.argv[2]

    if os.path.isfile(inpath):
        fastafilename = inpath
        qiimeformat_single_fasta(fastafilename, outpath)
    if os.path.isdir(inpath):
        infiles = [ fname for fname in os.listdir(inpath)
                    if fname.endswith('.fasta.gz') ]
        for fname in infiles:
            fastafilename = os.path.join(inpath, fname)
            print 'converting: %s' % fastafilename
            qiimeformat_single_fasta(fastafilename, outpath)


if __name__ == "__main__":
    main()    
