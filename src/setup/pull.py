#!/usr/bin/env python
## pull.py
#
# pull archived data from long term storage partition for analysis.
#
# @author Rahul Dhodapkar <rahul.dhodapkar@yale.edu>
# @version 2022.02.15
#

import yaml
import sys
import subprocess

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
    print('Syncing archive for {sample}...'.format(**x))
    source_file = cfg['file_templates']['external_archive_location'].format(**x)
    dest_file = cfg['file_templates']['archive_file'].format(**x)
    args = ['rsync', '-av', source_file, dest_file]
    
    print('... {} -> {}'.format(source_file, dest_file))
    print('... ' + ' '.join(args))
    status = subprocess.run(args)
    status.check_returncode()
    print('... OK'.format(status))

print('All done!')
