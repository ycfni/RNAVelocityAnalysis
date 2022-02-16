#!/usr/bin/env python
## collect_outfiles.py
#
# Collect output files from velocyto run, and also perform loom file merging
# for integration with Seurat analysis.
#

import loompy
import yaml
import sys
import shutil
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
    print('Collecting velocyto output for {sample}...'.format(**x))
    loom_src = cfg['file_templates']['velocyto_loom_file'].format(**x)
    loom_dst = cfg['file_templates']['velocyto_loom_file_export_loc'].format(**x)

    print('... creating job directories')
    out_dir = os.path.dirname(loom_dst)
    os.makedirs(out_dir, exist_ok=True)

    print('... copying loom files')
    shutil.copyfile(loom_src, loom_dst)

    print('... OK')

merged_loom_loc = cfg['file_templates']['velocyto_merged_export_loc']
loomloc_template = cfg['file_templates']['velocyto_loom_file_export_loc']
print('Merging loom files -> {}'.format(merged_loom_loc))
loompy.combine(
    [loomloc_template.format(**x) for x in cfg['data']]
    , merged_loom_loc
    , key='Accession')

print('All done!')

