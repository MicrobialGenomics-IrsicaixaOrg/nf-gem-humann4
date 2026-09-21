import csv
import sys
from pathlib import Path
trace=max(Path(sys.argv[1]).glob('execution_trace_*.txt'),key=lambda x:x.stat().st_mtime)
rows=list(csv.DictReader(trace.open(),delimiter='\t'))
assert rows and all(row['status']=='CACHED' for row in rows), rows
print(f'All {len(rows)} tasks resumed from cache')
