import unittest
from artemis_ranking import canonical,rerank,VERSION

def result(title,url,engines=None,positions=None,**kw):
    return dict(title=title,content=title,url=url,engines=engines or ['source'],positions=positions or [1],**kw)
class Ranking(unittest.TestCase):
    def test_relevant_beats_noise(self):
        noise=result('Sports today','https://sports.test/a');relevant=result('Swift WebKit browser documentation','https://docs.test/a')
        self.assertEqual(rerank('Swift WebKit',[noise,relevant])[0][0],relevant)
    def test_consensus(self):
        a=result('Moon','https://a.test');b=result('Moon','https://b.test',engines=['a','b','c'],positions=[1,2,3]);self.assertEqual(rerank('Moon',[a,b])[0][0],b)
    def test_ads_removed(self):
        for key in ['is_ad','sponsored','advertisement','is_sponsored']:
            self.assertEqual(rerank('x',[result('Ad','https://a.test',**{key:True})])[0],[])
    def test_dedupe_tracking(self):
        a=result('A','https://a.test/p?utm_source=x&x=1');b=result('A','https://a.test/p?x=1#top');self.assertEqual(len(rerank('a',[a,b])[0]),1);self.assertIn('utm_source',a['url'])
    def test_unsafe(self):
        for url in ['javascript:alert(1)','file:///etc/passwd','https://user:pass@a.test','https://a.test:bad']:
            self.assertIsNone(canonical(url))
    def test_diversity(self):
        pages=[result('Moon',f'https://a.test/{i}') for i in range(10)]+[result('Moon','https://b.test/a')]
        top=rerank('Moon',pages)[0][:3];self.assertTrue(any('b.test' in x['url'] for x in top))
    def test_deterministic(self):
        pages=[result('Moon','https://b.test'),result('Moon','https://a.test')];self.assertEqual(rerank('Moon',pages),rerank('Moon',pages))
    def test_no_mutation(self):
        a=result('<script>unsafe</script> Moon','https://a.test');before=dict(a);ordered,why=rerank('moon',[a]);self.assertIs(ordered[0],a);self.assertEqual(a,before);self.assertEqual(why[a['url']]['version'],VERSION)
    def test_lenses(self):
        for lens in ['balanced','research','discovery','invalid']:
            _,why=rerank('a',[result('A','https://a.test')],lens);self.assertIn(why['https://a.test']['lens'],['balanced','research','discovery'])
    def test_bounded(self):
        self.assertEqual(len(rerank('a',[result('A',f'https://a.test/{i}') for i in range(500)])[0]),300)
    def test_empty(self):self.assertEqual(rerank('',[]),([],{}))
    def test_missing_positions_explained(self):
        a=result('A','https://a.test');a.pop('positions');self.assertEqual(rerank('a',[a])[1][a['url']]['rank_basis'],'merged source order')
if __name__=='__main__':unittest.main()
