#!/usr/bin/env python3
"""Expose native HUMAnN log percentages as MultiQC custom data."""
import json
import re
import sys
from pathlib import Path

validation = json.loads(Path(sys.argv[1]).read_text())
log = Path(sys.argv[2]).read_text()
metrics = {'profile_sgbs': validation['sgbs']}
for stage in ['nucleotide', 'translated']:
    match = re.search(r'Unaligned reads after ' + stage + r' alignment:\s*([\d.]+)\s*%', log)
    if match:
        metrics[f'unaligned_after_{stage}_pct'] = float(match.group(1))
print(json.dumps({
    'id': 'humann4_alignment', 'section_name': 'HUMAnN 4 alignment QC',
    'description': 'SGBs in the input profile and native unaligned-read percentages from HUMAnN logs. Missing metrics remain absent.',
    'plot_type': 'table', 'pconfig': {'id': 'humann4_alignment_table', 'title': 'HUMAnN 4 alignment QC'},
    'data': {validation['sample']: metrics}
}, indent=2))
