#!/usr/bin/python

import sys
import os.path
import subprocess
from os import remove
import parse_mapfile
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--indir", dest="inpath",
       help="path to input dir")
parser.add_option("-m", "--mapfile", dest="mapfname",
       help="path to mapfile")
parser.add_option("-d", "--depth", dest="depth",
       type="int", default = 0,
       help="read depth sampled")
#parser.add_option("-r", "--reduce", default=False,
#       action="store_true",
#       help="switch to make to depth just an upper limit")
(options, args) = parser.parse_args()

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
    if depth and int(count) == depth:
        subprocess.call('cat {0} >> merged_seqs.fna'.format(tempfname),
                    shell=True)
        print '%s merged into merged_seqs.fna' % tempfname
    else:
         print count, ' not = ', depth, ' skipped!'

    remove(tempfname)
