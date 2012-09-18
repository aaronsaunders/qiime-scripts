#!/usr/bin/python

import sys
import os.path
import subprocess
from os import remove
import parse_mapfile

inpath = sys.argv[1]
mapfname = sys.argv[2]
depth = sys.argv[3]

# infiles
with open(mapfname, 'rU') as mapfh:
    mapdict = parse_mapfile.parse(mapfh)

inpaths = [ os.path.join(inpath, amplibID) + '.fna.gz'
            for amplibID in sorted(mapdict.keys()) ]

for fname in inpaths:
    stub = os.path.basename(fname)[:-7]
    tempfname = stub + '.fna'

    cmd = 'zcat {0} > {1}'.format(fname, tempfname)
    subprocess.call(cmd, shell=True)

    cmd = 'seqmagick mogrify --head {1} {0}'.format(tempfname, depth)
    subprocess.call(cmd, shell=True)

    result = subprocess.Popen("grep -c '^>' {0}".format(tempfname),
                              stdout=subprocess.PIPE, shell=True)
    (count, err) = result.communicate()
    if err:
       count = 0
    if int(count) == int(depth):
        subprocess.call('cat {0} >> merged_seqs.fna'.format(tempfname),
                    shell=True)
        print '%s merged into merged_seqs.fna' % tempfname
    else:
         print count, ' not = ', depth, ' skipped!'

    remove(tempfname)
