## Makefile
#
# Simple tool to package scripts commonly run together, to enable easy
# interactive use of the scripts in this repository.  Note that all scripts
# should be run on an interactive compute node with the appropriate
# conda environment enabled
#
# @author Rahul Dhodapkar <rahul.dhodapkar@yale.edu>
# @version 2022.02.15
#

.PHONY: pull check unpack stage submit

###############################################################################
## SETUP
###############################################################################

pull:
	echo "Syncing data from archive, may take some time."
	./src/setup/pull.py

check:
	echo "Checking archive integrity, may take some time."
	./src/setup/validate_integrity.py

unpack:
	echo "Unpacking tarballs, may take some time."
	./src/setup/unpack.py

###############################################################################
## ANALYSIS
###############################################################################

stage:
	echo "Staging slurm jobs"
	./src/analysis/stage_velocyto.py

submit:
	echo "Submit slurm jobs"
	./src/analysis/submit_jobs.py

