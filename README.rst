============================================================
Bioinformatics workflow for preprocessing Illumina amplicons
============================================================

The overall workflow:

- assemble reads with pandaseq
- filter out unique reads with low coverage
- reformat reads for qiime pipeline 

*Dependencies*
Must be installed and callable (binary added to $PATH):
 
- python 2.6 
- pandaseq (http://github.com/neufeld/pandaseq.git) 




Batch script
------------

If you are processing the sequences from different runs or folders copy all of the sequences to the same folder::

   python preprocess_illumina.py ~/work/raw ~/work/out 10

takes 3 arguments:
1. input directory
2. output directory
3. cutoff for unique reads coverage

runs the following scripts in order:



Assemble w. pandaseq
--------------------
Uses pandaseq to assemble all of the pairs of .fastq.gz files in the input directory.


pandaseq_batch.py::

	(pandaseq -f /space/sequences/Final_111221_SN1040_0049_AD0HVDACXX_1/Labscale-SBR-AMS A4-01_AAATCACG_L004_R1_001.fastq.gz -r /space/sequences/Final_111221_SN1040_0049_AD0HVDACXX_1/Labscale-SBR-AMS/A4-01_AAATCACG_L004_R2_001.fastq.gz -o 40 -t 0.9 -N | gzip > A4-01_AAATCACG_L004.fasta.gz ) 2> A4-01_AAATCACG_L004.log 


Filter unique reads with low coverage
-------------------------------------

count unique reads and then filter for unique reads that are present greater than a given threshold (default: 10)


REFORMAT for qiime
------------------
reformat_fasta_for_qiime



NOTE on Input files
-------------------

After demultiplexing the reads are saved on the file server accesible from Dragon/Donkey: 

/space/sequences/_RUN_/_PROJECT_/_filename_

**RUN name**

120207_SN1040_0050_AC0BY4ACXX_1

0. date
1. machine
2. consecutive run# for that machine
3. flowcell

**Project name**

From the sample sheet sent to Mads upon submission

**Filename**

A11-01_AAATCACG_L008_R1_001.fastq.gz

0. sampleID
1. barcode
2. lane#
3. R1/R2 = f/r
4. demultiplexing batch (this is usually "001" as we do not limit the file sixes of the demultiplexed reads)


