import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('validator', Path(__file__).parents[1]/'bin/validate_profile.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
INDEX = 'mpa_vOct22_CHOCOPhlAnSGB_202403'
HEADER = '#' + '\t'.join(validator.COLUMNS) + '\n'
ROW = 'k__Bacteria|s__Fixture|t__SGB1\t2||\t12\t0.01\t100\n'

class ProfileTests(unittest.TestCase):
    def check(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'profile.tsv'
            path.write_text(text)
            return validator.validate(path, INDEX)
    def test_original_extended_profile(self):
        self.assertEqual(self.check('#'+INDEX+'\n'+HEADER+ROW)['sgbs'],1)
    def test_rejects_wrong_database(self):
        with self.assertRaises(ValueError): self.check('#mpa_vJan25\n'+HEADER+ROW)
    def test_rejects_relative_abundance_only(self):
        with self.assertRaises(ValueError): self.check('#'+INDEX+'\n#clade_name\trelative_abundance\nx\t1\n')
    def test_rejects_nan_coverage(self):
        with self.assertRaises(ValueError): self.check('#'+INDEX+'\n'+HEADER+ROW.replace('0.01','nan'))
    def test_zero_sgbs_is_valid(self):
        self.assertEqual(self.check('#'+INDEX+'\n'+HEADER+'UNCLASSIFIED\t-1\t100\t-\t100\n')['sgbs'],0)
    def test_rejects_empty_profile(self):
        with self.assertRaises(ValueError): self.check('#'+INDEX+'\n'+HEADER)
