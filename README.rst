=============================================
Scripts for running qiime with Illumina reads
=============================================

Pre-processing
==============

Workflow:

1) pandaseq.py: assemble forward and reverse reads using pandaseq
2) unique.py: filter out unique reads not occuring more than a certain cutoff (default = 10)
3) reformat_fasta_for_qiime.py: reformat the fasta headers of the reads for qiime.


Dependencies:
python 2.6
pandaseq (http://github.com/neufeld/pandaseq.git)

There is a wrapper for the process (preprocess_illumina.py) that takes an input and output folder and a cutoff as arguments.

