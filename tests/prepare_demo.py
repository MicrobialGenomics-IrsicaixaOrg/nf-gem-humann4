#!/usr/bin/env python3
"""Prepare a small integration fixture from the pinned HUMAnN distribution.
The profile is synthetic, not an empirical MetaPhlAn result or a scientific test.
"""
import argparse
import gzip
import importlib.util
import shutil
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--humann-root', type=Path)
parser.add_argument('--output', type=Path, default=Path('tests/data'))
args = parser.parse_args()
root = args.humann_root or Path(importlib.util.find_spec('humann').origin).parent
out = args.output.resolve()
out.mkdir(parents=True, exist_ok=True)
for source, destination in [('chocophlan_DEMO','chocophlan_DEMO'), ('uniref_DEMO','protein'), ('utility_DEMO','utility')]:
    shutil.copytree(root/'data'/source, out/destination, dirs_exist_ok=True)
lines = (root/'tests/data/demo.fastq').read_bytes().splitlines(keepends=True)[:40000]
for name, content in [('demo_a_R1',lines[:20000]), ('demo_a_R2',lines[20000:]), ('demo_b',lines)]:
    with gzip.GzipFile(str(out/f'{name}.fastq.gz'), 'wb', mtime=0) as handle:
        handle.write(b''.join(content))
profile = '#mpa_vOct22_CHOCOPhlAnSGB_202403\n# Synthetic integration fixture; not a biological result\n'
profile += '#clade_name\tclade_taxid\trelative_abundance\tcoverage\testimated_number_of_reads_from_the_clade\n'
for sgb in ['1871','2091','2301']:
    profile += f'k__Bacteria|g__Fixture|s__Fixture_SGB{sgb}|t__SGB{sgb}\t2||||\t33.333\t0.1\t1000\n'
(out/'profile.tsv').write_text(profile)
(out/'samplesheet.csv').write_text('sample,fastq_1,fastq_2,taxonomic_profile\n'
    + f'demo_a,{out}/demo_a_R1.fastq.gz,{out}/demo_a_R2.fastq.gz,{out}/profile.tsv\n'
    + f'demo_b,{out}/demo_b.fastq.gz,,{out}/profile.tsv\n')
