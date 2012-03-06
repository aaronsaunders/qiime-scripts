#!/bin/sh

otu='otu02'
seqs='../clean/TIT003_clean.fna'
cores='5'
map='/home/user/ams/Dropbox/projects/TIT003/mappingfile.txt'
param='custom_parameters.txt'

pick_otus_through_otu_table.py -i $seqs -o $otu -p $param -a -O $cores

summarize_taxa_through_plots.py -i $otu/otu_table.txt -o taxa_summary -m $map -p $param

echo "alpha_diversity:metrics shannon,PD_whole_tree,chao1,observed_species" > alpha_params.txt

alpha_rarefaction.py -i $otu/otu_table.txt -m $map -o alpharar/ -p alpha_params.txt -t $otu/rep_set.tre -a -O $cores -f

mv alpha_params.txt ./alpharar/ 

beta_diversity_through_plots.py -i $otu/otu_table.txt -m $map -o betadiv_even2300/ -t $otu/rep_set.tre -e 2300 -a -O $cores -f

cp $map ./

mv $otu/otu_table.txt ./betadiv_even12k/otu_table* .