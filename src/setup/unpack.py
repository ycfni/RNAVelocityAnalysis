#!/usr/bin/env python
## unpack.py
#
# Unpack all archives and ready for velocyto run.
#
# @author Rahul Dhodapkar <rahul.dhodapkar@yale.edu>
# @version 2022.02.15
#

import tarfile
import yaml
import sys

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
    print('Extracting {sample}...'.format(**x))
    archive_path = cfg['file_templates']['archive_file'].format(**x)
    extract_archive_to = cfg['file_templates']['extract_archive_to'].format(**x)

    print('... unpacking {} -> {}'.format(archive_path, extract_archive_to))
    with tarfile.open(archive_path,'r') as tf:
        tf.extractall(path=extract_archive_to)

    print('... done')

print('All done!')

