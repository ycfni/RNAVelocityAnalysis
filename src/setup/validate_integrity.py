#!/usr/bin/env python
## validate_integrity.py
# 
# Simple script to validate the integrity of files prior to running analysis.
# Intended to be run from the root directory, depends on config.yml `data`
# block as well as the `file_templates` block.
#
# @author Rahul Dhodapkar <rahul.dhodapkar@yale.edu>
# @version 2022.02.15
#

import hashlib
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

failed_data_validation = []
for x in cfg['data']:
    print('Validating {sample}...'.format(**x))
    md5_sumfile = cfg['file_templates']['md5_sumfile'].format(**x)
    archive_file = cfg['file_templates']['archive_file'].format(**x)
    
    print('... loading hash')
    # get hash value from file
    stored_hash = None
    with open(md5_sumfile, 'r') as f:
        stored_hash = f.readline().split()[0] 
    if stored_hash is None:
        print('Failed, unable to read md5 hash file', file=sys.stderr)
        sys.exit(1)
    print('... hash = {} (stored)'.format(stored_hash))

    print('... hashing archive')
    calc_hash = None
    md5_hash = hashlib.md5()
    with open(archive_file,'rb') as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096),b''):
            md5_hash.update(byte_block)
        calc_hash = md5_hash.hexdigest()
    if calc_hash is None:
        print('Failed, unable to compute md5 hash on archive', file=sys.stderr)
        sys.exit(1)
    print('... hash = {} (calc)'.format(calc_hash))

    print('... checking hashes')
    if calc_hash != stored_hash:
        failed_data_validation.append(x['sample'])
        print('... FAILED {} (stored) != {} (calc)'.format(stored_hash, calc_hash))
    else:
        print('... OK')

if len(failed_data_validation) != 0:
    print('Some samples failed validation', file=sys.stderr)
    print(failed_data_validation, file=sys.stderr)
    sys.exit(1)

print('All done!')
