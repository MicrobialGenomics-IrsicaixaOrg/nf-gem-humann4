"""Check actual integration results; this intentionally fails on stub output."""
import csv
import json
import sys
from pathlib import Path
root=Path(sys.argv[1])
for sample in ['demo_a','demo_b']:
    folder=root/'humann4'/sample
    assert json.loads((folder/f'{sample}_validation.json').read_text())['sgbs']==3
    log=(folder/f'{sample}_0.log').read_text()
    assert 'Running humann v4.0.0' in log
    assert 'running metaphlan' not in log.lower()
    for suffix in ['2_genefamilies','3_reactions','4_pathabundance']:
        f=folder/f'{sample}_{suffix}.tsv'
        assert f.stat().st_size>0, f
for kind in ['genefamilies','reactions','pathabundance']:
    table=root/'tables'/f'{kind}.tsv'
    with table.open() as handle:
        rows=list(csv.reader(handle,delimiter='\t'))
    assert len(rows[0])==3, rows[0]
    assert any('demo_a' in x for x in rows[0]) and any('demo_b' in x for x in rows[0])
    for row in rows[1:]:
        assert len(row)==3
        for value in row[1:]: assert float(value)>=0
    assert (root/'tables'/f'{kind}_unstratified.tsv').exists()
    assert (root/'tables'/f'{kind}_stratified.tsv').exists()
assert (root/'multiqc/multiqc_report.html').exists()
print('Real HUMAnN integration outputs verified')
