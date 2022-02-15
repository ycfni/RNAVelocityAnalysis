#!/usr/bin/env python
## stage_velocyto.py
#
# Build all slurm scripts for running velocyto
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

velocyto_slurm_template = None
with open('./slurm_templates/velocyto_slurm.fs', 'r') as f:
    velocyto_slurm_template = f.read()
if velocyto_slurm_template is None:
    print('Failed to load "velocyto_slurm.fs" template', sys.stderr)
    sys.exit(1)

print(velocyto_slurm_template)
for x in cfg['data']:
    print('Staging velocyto slurm job for {sample}...'.format(**x))
    job_dir = cfg['file_templates']['velocyto_slurm_job_dir'].format(**x)
    template_params = \
            {k:v.format(**x) for (k,v) in cfg['file_templates'].items()} \
            | cfg['user_info'] \
            | cfg['runtime'] \
            | x \
            | {'cwd': os.getcwd()}
    
    print('... creating job directories')
    os.makedirs(job_dir, exist_ok=True)

    print('... writing slurm job script')
    with open(job_dir + '/run_velocyto.sh', 'wt') as f:
        f.write(velocyto_slurm_template.format(**template_params))
    print('... done')
    
print('All done!')

