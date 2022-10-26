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
        
        import os
        
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tf, path=extract_archive_to)

    print('... done')

print('All done!')

