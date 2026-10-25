import unittest
from artemis_query import plan,narrow
class Hashtags(unittest.TestCase):
 def test_lens(self):self.assertEqual(plan('moon #research')['lens'],'research')
 def test_category(self):self.assertEqual(plan('moon #news',{'category_general':'1'})['form'],{'q':'moon','categories':'news'})
 def test_time(self):self.assertEqual(plan('moon #week')['form']['time_range'],'week')
 def test_topic_required(self):
  p=plan('moon #astronomy');self.assertEqual(len(narrow([{'title':'moon astronomy','url':'https://a.test'},{'title':'moon cake','url':'https://b.test'}],p)),1)
 def test_site_boundary(self):
  p=plan('swift #site:apple.com');self.assertEqual(len(narrow([{'url':'https://developer.apple.com'},{'url':'https://apple.com.evil.test'}],p)),1)
 def test_code_hash(self):self.assertEqual(plan('C# tutorial')['effective'],'C# tutorial')
 def test_language(self):self.assertEqual(plan('moon #lang:en')['form']['language'],'en')
 def test_unknown_operator_not_injected(self):self.assertIn('#site:evil/path',plan('moon #site:evil/path')['effective'])
 def test_docs(self):self.assertEqual(len(narrow([{'title':'Manual','url':'https://a.test'},{'title':'Shop','url':'https://b.test'}],plan('swift #docs'))),1)
 def test_no_mutation(self):
  form={'q':'moon #week'};plan(form['q'],form);self.assertEqual(form,{'q':'moon #week'})
