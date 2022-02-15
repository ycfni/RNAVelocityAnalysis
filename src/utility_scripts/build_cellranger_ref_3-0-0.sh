#!/usr/bin/env bash
#
# Build cellranger homo sapiens reference version 3.0.0
#
# See: https://support.10xgenomics.com/single-cell-gene-expression/software/release-notes/build#grch38_3.0.0
#
# Notes:
#   This script takes a significant amount of memory to run, especially to
#   build the STAR index on the human reference sequence.
#
#   Tested on a node with 64GB of RAM and 8 CPU. Can be allocated for
#   interactive use with slurm command
#
#       srun --pty --mem-per-cpu=8000 --cpus-per-task=8 -p interactive bash
#
# Usage:
#   Manually create a directory in which you would like to build your reference (e.g. ~/scratch60/ref)
#   and navigate to it in an interactive shell session.  Then, run this script from inside the
#   newly created folder.
#
# @author Rahul Dhodapkar <rahuldhodapkar>
# @version 2022.02.15
#

set -x
set -e

module load cellranger/3.1.0
module load STAR/2.7.7a-GCCcore-10.2.0
source ${EBROOTCELLRANGER}/sourceme.bash

wget ftp://ftp.ensembl.org/pub/release-93/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
gunzip Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz


wget ftp://ftp.ensembl.org/pub/release-93/gtf/homo_sapiens/Homo_sapiens.GRCh38.93.gtf.gz
gunzip Homo_sapiens.GRCh38.93.gtf.gz


cellranger mkgtf Homo_sapiens.GRCh38.93.gtf Homo_sapiens.GRCh38.93.filtered.gtf \
                 --attribute=gene_biotype:protein_coding \
                 --attribute=gene_biotype:lincRNA \
                 --attribute=gene_biotype:antisense \
                 --attribute=gene_biotype:IG_LV_gene \
                 --attribute=gene_biotype:IG_V_gene \
                 --attribute=gene_biotype:IG_V_pseudogene \
                 --attribute=gene_biotype:IG_D_gene \
                 --attribute=gene_biotype:IG_J_gene \
                 --attribute=gene_biotype:IG_J_pseudogene \
                 --attribute=gene_biotype:IG_C_gene \
                 --attribute=gene_biotype:IG_C_pseudogene \
                 --attribute=gene_biotype:TR_V_gene \
                 --attribute=gene_biotype:TR_V_pseudogene \
                 --attribute=gene_biotype:TR_D_gene \
                 --attribute=gene_biotype:TR_J_gene \
                 --attribute=gene_biotype:TR_J_pseudogene \
                 --attribute=gene_biotype:TR_C_gene


cellranger mkref --genome=GRCh38 \
                 --fasta=Homo_sapiens.GRCh38.dna.primary_assembly.fa \
                 --genes=Homo_sapiens.GRCh38.93.filtered.gtf \
                 --ref-version=3.0.0

# copy repetitive elements mask for GRCh38, originall downloaded from UCSC Genome Browser
cp /SAY/standard/ycfni01-CC1410-MEDPAT/rd389/reference_data/GRCh38_rmsk/GRCh38_rmsk.gtf ./

echo "All done!"

