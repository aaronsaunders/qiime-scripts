#!/usr/bin/python

import sys
import os.path
import gzip


def zreformat_fastq_for_qiime(filepath):
    """
    reformats the Illumina fastq headers output by pandaseq to headers
    compatible with qiime (identical to qiime spilt_libraries.py).

    @HWI-ST1040:49:D0HVDACXX:4:1101:6323:2652:AAATCACG
    TACGGGGGGAGCAAGCG...

    >AMPA069_1 HWI-ST1040:49:D0HVDACXX:4:6323:2652 orig_bc=AAACTTGA 
            new_bc= AAACTTGA bc_diffs=0
    TACGGGGGGAGCAAGCG...
    
    """
    filename = os.path.basename(filepath)
    sample = filestub = filename[:-9]
    count = 0
    try:
        fastqfile = gzip.open(filepath, 'rb')
    except:
        print 'could not open infile %s' % filepath
    try:
        fastafile = gzip.open(sample + '.fna.gz', 'wb')
    except:
        print 'could not open outfile %s' % sample

    while True:
        line = fastqfile.readline()
        if not line:
            break
        line = line.strip()
        if line.startswith('@'):
            read_id, colon, barcode = line.rpartition(':')
        else:
            continue
        seq = fastqfile.readline()
        fastqfile.readline()
        fastqfile.readline()
        header = '>{sample}_{count} {read} orig_bc={barcode} new_bc= {barcode} bc_diffs=0\n'.format(
                sample=sample, read=read_id[1:], 
                barcode=barcode, count=count)
        fastafile.write(header + seq)
        count += 1
     
    fastqfile.close()
    fastafile.close()
    print '{0}\t{1}'.format(sample, count)

    return count


def main():

    infilepath = sys.argv[1]
    outfilepath = sys.argv[2]

    print
    print 'running ' + sys.argv[0]
    print 'indir: ' + infilepath
    print 'outdir:' + outfilepath
    
    if not os.path.isdir(infilepath):
        print 'sequence directory not found'
        sys.exit()

    fnames = ( [ fname for fname in os.listdir(infilepath) 
                              if fname.endswith('.fastq.gz') ] )
    print fnames
    if not os.path.isdir(outfilepath):
        os.mkdir(outfilepath)
    os.chdir(outfilepath)    
    print 'Converting!\n'
    print 'sample\tcount'

    for fname in fnames:
        inpath = os.path.join(infilepath, fname)
        zreformat_fastq_for_qiime(inpath)
        

if __name__ == '__main__':
    main()
