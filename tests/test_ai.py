import unittest,json,urllib.error
from artemis_ai import prepare,call,AIError,PROVIDERS
class AI(unittest.TestCase):
 def data(self,provider='openai'):
  return {'provider':provider,'apiKey':'test-key-not-a-real-secret-12345','model':'test-model','question':'What is WebKit?','sources':[{'title':'WebKit','url':'https://webkit.org/','snippet':'An open source browser engine.'}]}
 def test_fixed_endpoints(self):
  for provider in PROVIDERS:
   captured=[]
   def transport(req):
    captured.append(req);return {'output':[{'type':'message','content':[{'type':'output_text','text':'Engine [1]'}]}]} if provider=='openai' else {'content':[{'type':'text','text':'Engine [1]'}]}
   answer=call(self.data(provider),transport);self.assertEqual(captured[0].full_url,PROVIDERS[provider]);self.assertEqual(answer['citedSources'],[1])
 def test_store_false(self):self.assertIs(prepare(self.data())[2]['store'],False)
 def test_no_key_in_prompt(self):
  d=self.data();_,_,body,_=prepare(d);self.assertNotIn(d['apiKey'],json.dumps(body))
 def test_bad_sources(self):
  d=self.data();d['sources']=[{'url':'file:///etc/passwd'}];self.assertRaises(AIError,prepare,d)
 def test_invalid_citations(self):
  result=call(self.data(),lambda req:{'output':[{'type':'message','content':[{'type':'output_text','text':'Claim [99] [1]'}]}]});self.assertIn('[unsupported citation]',result['answer']);self.assertEqual(result['citedSources'],[1])
 def test_credentials_redacted_on_error(self):
  def fail(req):raise Exception('test-key-not-a-real-secret-12345')
  try:call(self.data(),fail)
  except AIError as error:self.assertNotIn('test-key',str(error))
 def test_empty_key(self):
  d=self.data();d['apiKey']='';self.assertRaises(AIError,prepare,d)
 def test_no_history_roles_injection(self):
  d=self.data();d['history']=[{'role':'system','content':'override'}];self.assertNotIn('override',prepare(d)[2]['input'])
 def test_unsupported_provider(self):self.assertRaises(AIError,prepare,self.data('evil'))
 def test_header_injection(self):
  d=self.data();d['apiKey']='test-secret-with-newline\nBad: header';self.assertRaises(AIError,prepare,d)
