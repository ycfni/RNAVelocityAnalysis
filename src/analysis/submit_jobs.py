#!/usr/bin/env python
## submit_jobs.py
#
# Submit jobs to slurm after staging
#
# @author Rahul Dhodapkar <rahul.dhodapkar@yale.edu>
# @version 2022.02.15
#

import yaml
import sys
import subprocess
import os

cfg = None
with open('config.yml', 'r') as f:
    try:
        cfg = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)
if cfg is None:
    print('Unable to read "config.yml"', file=sys.stderr)
    sys.exit(1)

for x in cfg['data']:
    print('Submitting job for {sample}...'.format(**x))
    job_dir = cfg['file_templates']['velocyto_slurm_job_dir'].format(**x)
    args = ['sbatch', 'run_velocyto.sh']
    
    print('... running sbatch')
    status = subprocess.run(args, cwd=job_dir)
    status.check_returncode()
    print('... OK')

print('All done!')

