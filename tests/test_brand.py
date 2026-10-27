# SPDX-License-Identifier: GPL-3.0-or-later
import unittest,json,hashlib
from pathlib import Path
class Brand(unittest.TestCase):
 def test_exact_canonical_assets(self):
  root=Path(__file__).resolve().parents[1]/'vigiltech';manifest=json.loads((root/'UPSTREAM.json').read_text())
  self.assertEqual(manifest['commit'],'30186592391b296d788f29b411d5701ef4f972e3')
  for name,digest in manifest['sha256'].items():self.assertEqual(hashlib.sha256((root/name).read_bytes()).hexdigest(),digest,name)
 def test_search_bridge_keeps_visible_heading_and_new_namespace(self):
  root=Path(__file__).resolve().parents[1];css=(root/'vigiltech-search.css').read_text()
  self.assertIn('visibility:visible!important',css)
  for old in ['--cs-','--vt-green-','.artemis-','.altstack-']:self.assertNotIn(old,css)
  self.assertIn('var(--vt-pink-600)',css);self.assertIn('prefers-reduced-transparency',css)
  self.assertIn('Vigil Search',(root/'brand.py').read_text())
