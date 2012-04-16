#!/bin/sh
###
### Job name
#SBATCH --job-name=illumina
### Name of queue to submit to
###SBATCH --partition killing
### Time limit of total run time of the job
###SBATCH --time=20:00:00
### Number of processor cores
#SBATCH -n 20
#SBATCH --error=slurm-%j.err
### The actual job execution

seqs='./data/A4-06_AAGCCAAT_L004_R1_001.fasta'
cores='20'
map='./mapfile.txt'
param='./custom_parameters.txt'
resample=25000

outroot='./res/run01'

echo 'checking mapping file'
check_id_map.py -m mapfile.txt -o mapcheck -v
# mapfile checked

# echo 'unzipping'
#gunzip ./data/A4-06_AAGCCAAT_L004_R1_001.fastq.gz
echo 'unzipped'
# echo 'reformatting'
#python ./scr/reformat_fastq_for_qiime.py ./data/A4-06_AAGCCAAT_L004_R1_001.fastq ./data/A4-06_AAGCCAAT_L004_R1_001.fasta
echo 'reformatted'

echo 'picking otus'
pick_otus_through_otu_table.py -i $seqs -o $outroot/otu -p $param -a -O $cores

echo 'summarize taxa'
summarize_taxa_through_plots.py -i $outroot/otu/otu_table.txt -o $outroot/taxa_summary -m $map -p $param

echo "alpha_diversity:metrics shannon,PD_whole_tree,chao1,observed_species" > alpha_params.txt

echo 'alpha rarefaction'
alpha_rarefaction.py -i $outroot/otu/otu_table.txt -m $map -o $outroot/alpharar/ -p alpha_params.txt -t $outroot/otu/rep_set.tre -a -O $cores -f

mv alpha_params.txt ./$outroot/alpharar/ 

echo 'calculating beta div'
beta_diversity_through_plots.py -i $outroot/otu/otu_table.txt -m $map -o $outroot/betadiv/ -t $outroot/otu/rep_set.tre -e $resample -a -O $cores -f

echo 'finishing'
cp $map $param $outroot

mv $outroot/otu/otu_table.txt ./$outroot/betadiv/otu_table* ./$outroot

echo 'DONE!'