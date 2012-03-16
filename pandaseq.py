
#!/usr/bin/python
# ams@bio.aau.dk

import sys
import subprocess
import gzip
import os
import os.path

def zcount_fastq(filepath):
    """
    counts the reads in a fastq file in a naive way 
    (I used this method due to problems with the use of @ in 
    the qual string for this version of fastq) 
    """
    count = 0

    fh = gzip.open(filepath, 'rb')
    for line in fh:
        if not line.startswith('@'):
            continue
        line = line.rstrip()

        count += 1
        fh.readline()
        fh.readline()
        fh.readline()
              
    fh.close()
    
    return count

def assemble_reads_pandaseq(fread, rread, overlap, outfilestub):
    """calls pandaseq in a shell
    """
    outfilename = outfilestub + '.fastq.gz'
    logfh = open(outfilestub + '.log', 'w')

    cmd = 'pandaseq -f {0} -r {1} -N -o {2} -F | gzip > {3}'.format(
                                 fread, rread, overlap, outfilename)
    print cmd
    pandaseq = subprocess.Popen(cmd, shell=True, stderr=logfh)
    pandaseq.wait()
    
    logfh.close()
    
    return

    
def main():

    overlap = 40
    threshold = 0.9
    
    # parse filenames and match F and R reads in pairs. 

    sequence_dir = sys.argv[1]
    print 'inpath: ' + sequence_dir
    outfilepath = sys.argv[2]
    print 'outpath: ' + outfilepath
    print 'overlap: ' + overlap
    print 'threshold: ' + threshold+ '\n'
    try:
        assert os.path.isdir(sequence_dir) is True
    except AssertionError:
        print 'sequence directory not found'
        sys.exit()
    
    seqfnames = ( [ fname for fname in os.listdir(sequence_dir) 
                              if fname.endswith('.fastq.gz') ] )

    samples = {}
    for fname in seqfnames:
        name, read_direction = fname.split('_')[0], fname.split('_')[3]
        fullpath = os.path.join(sequence_dir, fname)
        
        if name not in samples:
            samples[name] = {}
        samples[name][read_direction] = fullpath

    # Assert that all have a f and r
    # log the pairs and unmatched
    for sampleID, fnames in samples.items():
        if len(fnames.keys()) != 2:
                del samples[sampleID]
                print ('sample {0} not assembled due to name pars 
                                            error'.format(sampleID))
    sample_keys = [ sampleID for sampleID in samples.keys() ]
    print 'The following filenames will be assembled:'
    for sample in sorted(sample_keys):
        print sample
    print '\n'

    # run pandaseq on each pair
    try:
        assert os.path.isdir(outfilepath) is True
    except AssertionError:
        os.mkdir(outfilepath)
    os.chdir(outfilepath)    

    for sample in sorted(sample_keys):
        print 'assembling sample: {0}'.format(sample)
        fread = samples[sample]['R1']
        rread = samples[sample]['R2']

        count = zcount_fastq(fread)
        assemble_reads_pandaseq(fread, rread, overlap, sample)
        assembled = zcount_fastq(sample + '.fastq.gz')
        percent_assembled = float(assembled) / count * 100

        print '{0} of {1} ({2}%) assembled\n'.format(
                             assembled, count, round(percent_assembled))

if __name__ == '__main__':
    main()

