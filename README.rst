The following is a quick summary of the helper scripts I use with qiime
(qiime.org).


gather_seqs.py
--------------
usage: gather_seqs.py -i input_dir -m mapfile [-d exact] [-r reduce] 

Takes a mapfile and an input directory containing fasta files. Each file
must correspond to the Sample_id (first column) in the mapfile:

Sample_ID	filename
AMPA120		AMPA120.fna.gz
 
Each sample and merges the sequences into a seq.fna file for analysis. 
The script can additionally resample at max the given depth (-r number) 
or at exactly the given depth (-d number) which removes samples that do 
not contain sufficient reads. 

parse_mapfile.py
----------------
usage: parse_mapfile(mapfile_fh)

module for parsing mapfile to a dict
