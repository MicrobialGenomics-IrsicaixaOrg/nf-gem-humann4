#!/usr/bin/env python3
"""Validate an unchanged MetaPhlAn profile before spending alignment time."""
import json
import math
import sys
from pathlib import Path

COLUMNS = ['clade_name', 'clade_taxid', 'relative_abundance', 'coverage',
           'estimated_number_of_reads_from_the_clade']

def validate(path, index):
    header = None
    version = None
    rows = 0
    sgbs = 0
    seen = set()
    for line in Path(path).read_text().splitlines():
        if not line.strip():
            continue
        if line.startswith('#mpa_v'):
            version = line[1:].strip()
        if line.startswith('#clade_name\t'):
            header = line[1:].split('\t')
            if header != COLUMNS:
                raise ValueError('Expected rel_ab_w_read_stats columns in their original order')
        if line.startswith('#'):
            continue
        if header is None:
            raise ValueError('Missing rel_ab_w_read_stats column header')
        fields = line.split('\t')
        if len(fields) != len(COLUMNS):
            raise ValueError('Malformed profile row')
        rows += 1
        if fields[0] in seen:
            raise ValueError('Duplicate taxon in individual profile')
        seen.add(fields[0])
        if '|t__' in fields[0]:
            if float(fields[2]) > 100:
                raise ValueError('Relative abundance must not exceed 100 percent')
            for value in fields[2:]:
                number = float(value)
                if not math.isfinite(number) or number < 0:
                    raise ValueError('Abundance, coverage and estimated counts must be finite and nonnegative')
            sgbs += 1
    if version != index:
        raise ValueError(f'Expected database {index}, found {version}')
    if header is None or rows == 0:
        raise ValueError('Empty or merged profile; provide the individual MetaPhlAn output')
    # Zero detected SGBs are valid: HUMAnN can use translated search alone.
    return {'metaphlan_index': version, 'rows': rows, 'sgbs': sgbs}

if __name__ == '__main__':
    try:
        result = validate(sys.argv[1], sys.argv[2])
        result['sample'] = sys.argv[3]
        print(json.dumps(result, indent=2))
    except (ValueError, IndexError, OSError) as exc:
        sys.exit(f'Invalid MetaPhlAn profile: {exc}')
