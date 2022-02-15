#!/bin/bash
#SBATCH --partition={partition}
#SBATCH --job-name={sample}_velocyto
#SBATCH --cpus-per-task=12
#SBATCH --mem=100000
#SBATCH --time=36:00:00
#SBATCH --mail-type={mail_type}
#SBATCH --mail-user={email}

set -e 
set -x

module load miniconda
module load cellranger/6.0.1
module load SAMtools/1.13-GCCcore-10.2.0

cd {cwd}
conda activate {conda_env_name}

velocyto run10x -m {repeat_mask_location} {cellranger_outdir} {cellranger_gtf_location}

echo "All done!"
