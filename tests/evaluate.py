"""Small synthetic regression benchmark; not a production comparison."""
import math,sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from artemis_ranking import rerank
CASES=[
 ('swift webkit', [('Football results',0),('Swift tutorial',1),('WKWebView Swift WebKit documentation',3),('WebKit release notes',2)]),
 ('moon telescope', [('Latest sports',0),('Buy household goods',0),('Moon telescope observing guide',3),('Telescope optics handbook',2)]),
 ('markdown notes', [('Notes music',1),('Markdown notes app documentation',3),('Car maintenance',0),('Markdown editing reference',2)]),
 ('accessible interface', [('Accessible interface design guidelines',3),('Interface type in programming',1),('Recipes',0),('Accessible keyboard interface',2)]),
]
values=[]
for query,docs in CASES:
 candidates=[dict(title=title,content=title,url=f'https://source{i}.test/page',engines=['fixture'],positions=[i+1]) for i,(title,_) in enumerate(docs)]
 grades={c['url']:grade for c,(_,grade) in zip(candidates,docs)};ordered,_=rerank(query,candidates)
 def dcg(gs):return sum((2**g-1)/math.log2(i+2) for i,g in enumerate(gs[:5]))
 actual=[grades[c['url']] for c in ordered];ideal=sorted(grades.values(),reverse=True)
 ndcg=dcg(actual)/dcg(ideal);mrr=next((1/(i+1) for i,g in enumerate(actual) if g==3),0)
 values.append((ndcg,mrr))
 print(json.dumps({'query':query,'ndcg@5':round(ndcg,4),'reciprocal_rank':mrr}))
mean=sum(x[0] for x in values)/len(values)
print(json.dumps({'dataset':'synthetic regression v1, 4 queries / 16 snippets','mean_ndcg@5':round(mean,4),'mrr':sum(x[1] for x in values)/len(values),'comparative_claim':False}))
if mean<0.80:raise SystemExit('Synthetic relevance regression')
