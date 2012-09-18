#!/usr/bin/python
# ams@bio.aau.dk

import sys

def parse(mapfh):
    """
    helper to parse qiime mapping files
    usage: parse(<mappingfile_handle>)

    returns dict with:
        sampleID as key
        columns as values: (param, value) tuples
    """
    mapdict = {}

    # first line is header
    line = mapfh.readline()
    if line.startswith('#'):
        headers = [ header for header
                    in line[1:].rstrip().split('\t')[1:] ]
        colnum = len(headers)
    else:
        print 'mapfile has no header'
        sys.exit()

    # followed by none or more comment lines (sent to stdout)
    line = mapfh.readline()
    
    if line.startswith('#'):
        line = mapfh.readline()
        print line

    # then the mapping data
    while line:
        columns = line.rstrip().split('\t')
        if not len(columns) == (colnum + 1):
            sys.exit('uneven number of columns in some rows')
        parsed_row = []

        sampleID = columns.pop(0)
        for n in xrange(colnum):
            param = (headers[n], columns[n])
            parsed_row.append(param)
            mapdict[sampleID] = parsed_row

        line = mapfh.readline()

    return mapdict

