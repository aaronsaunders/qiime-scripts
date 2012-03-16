#!/usr/bin/python

import sys
import os.path
import gzip


def zreformat_fastq_for_qiime()
    """
    reformats the Illumina fastq headers output by pandaseq to headers
    compatible with qiime (identical to qiime spilt_libraries.py).

    @HWI-ST1040:49:D0HVDACXX:4:1101:6323:2652:AAATCACG
    TACGGGGGGAGCAAGCG...

    >AMPA069_1 HWI-ST1040:49:D0HVDACXX:4:6323:2652:1 orig_bc=AAACTTGA 
            new_bc= AAACTTGA bc_diffs=0
    TACGGGGGGAGCAAGCG...
    
    """
    count = 0
    written = 0

    with gzip.open(fastqfilename, 'rb') as fastqfile:
        outfile = gzip.open(outfilename, 'wb')

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
            id = '>{sample}_{count} {seqid}:{read} orig_bc={barcode} \
                    new_bc= {barcode} bc_diffs=0\n'.format(
                    sample=sample, seqid=seqid[1:], 
                    read=read, barcode=barcode, 
                    count=count)
            outfile.write(id + seq)
            written += 1

        print
        outfile.close()
        print 'reformatted {0} of {1} sequences'.format(written, count)
    return


def main():

    infilepath = sys.argv[1]
    outfilepath = sys.argv[2]

    print 'running ' + args[0]
    print 'infile: ' + infilepath
    print 'convert outfile:' + outfilepath
    
    if not os.path.isdir(sequence_dir):
        print 'sequence directory not found'
        sys.exit()

    fnames = ( [ fname for fname in os.listdir(infilepath) 
                              if fname.endswith('.fastq.gz') ] )
    
    if not os.path.isdir(outfilepath):
        os.mkdir(outfilepath)
    os.chdir(outfilepath)    

    for fname in fnames:
        inpath = os.path.join(infilepath, fname)
        zreformat_fastq_for_qiime(infile)
        

if __name__ == '__main__':
    main()
