"""Keep the default image compatible with the AWS Batch image-name parser."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]

class ContainerTests(unittest.TestCase):
    def test_digest_only_default_matches_schema(self):
        config = (ROOT / 'nextflow.config').read_text()
        image = re.search(r"humann_container\s*=\s*'([^']+)'", config).group(1)
        self.assertRegex(image, r"^[a-zA-Z0-9./_-]+@sha256:[0-9a-f]{64}$")
        schema = json.loads((ROOT / 'nextflow_schema.json').read_text())
        defaults = []
        def collect(node):
            if isinstance(node, dict):
                if 'humann_container' in node:
                    defaults.append(node['humann_container']['default'])
                for value in node.values():
                    collect(value)
        collect(schema)
        self.assertEqual(defaults, [image])
