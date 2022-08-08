# RNAVelocityAnalysis

Contains a set of scripts for generating RNA velcity data for incorporation
into single cell sequencing analysis pipelines.

The current repository is configured to analyze single-nucleus sequencing data
from glaucomatous and healthy human retina.  If you would like to adapt this
code for use in your own project, it can be done through modification of a few
metadata files.  Please contact the original author: 
[Rahul Dhodapkar](mailto:rahul.dhodapkar@yale.edu) and he can help walk you
through how to set up additional analysis.

## Setup
This analysis pipeline ultimately requires some representation of aligned
reads, often a BAM file.  These files are often *not* persisted and must
be regenerated from FASTQ files at the time of analysis.

A `utility_scripts` folder is provided under the `src` directory for some
scripts that may be useful in generating your BAM files from Fastq.  However,
the precise configuration parameters for sequence alignment should be
tailored to your specific use case and platform.

### `config.yml`
The `config.yml` file contains configuration settings for running velocyto
analysis.

The `user_info` block contains user information that is used during the
generation of jobs.

The `runtime` block contains configuration settings needed at runtime. For
example, settings for `python`, partition information for slurm jobs, etc.

The `file_templates` config block contains python template strings that are used
in the validation of data and orchestration of slurm jobs.  These are
provided mostly in the case that shared data may not have precisely the same
format as expected by these scripts.

The `data` block contains metadata for samples to run.  Note that template
strings and templated job files will directly depend on variable names
defined within the data block per sample.

### Reference Files
The genome reference files used by velocyto may be downloaded using
[this gist](https://gist.github.com/rahuldhodapkar/376ad1e0396b024f6521fc1beaf388c0).
The repeat mask file should be downloaded from the UCSC
Genome Browser, following the instructions from the velocyto documentation
[linked here](https://velocyto.org/velocyto.py/tutorial/cli.html#download-expressed-repeats-annotation)

## Additional Configuration
All code should run within a python `conda` environment, and has been tested
on the Yale HPC Ruddle cluster.

To create the conda environment, run:

    conda env create -f environment.yml

The conda environment created for this repository is named `rna_velocity`
and once installed can be activated for interactive use with the command

    conda activate rna_velocity

Unfortunately, due to several issues with conda forge, several dependencies
must still be installed via PyPI.  To install these, simply run

    pip install -r requirements.txt

after activating the `rna_velocity` conda environment.

## Usage
To make interaction with the system easier, scripts have been packaged
into discrete runnable chunks with the `make` utility.  Please take a look
at the `Makefile` in the root directory to see a list of all possible
commands.



