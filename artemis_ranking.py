# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright 2026 Cohnsoft.
"""Cohnsoft Search v1: deterministic, request-scoped candidate reranking.

Original implementation of published RRF, BM25 and MMR-style diversification.
No click tracking, identity, paid boosts, remote ranker, or page fetching.
"""
import math
import re
from collections import Counter
from html import unescape
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

VERSION = 'artemis-rank-1'
LENSES = {'balanced', 'research', 'discovery'}
TRACKING = {'fbclid', 'gclid', 'dclid', 'msclkid', 'mc_cid', 'mc_eid'}

def plain(value):
    return unescape(re.sub(r'<[^>]*>', ' ', str(value or '')))[:6000]

def tokens(value):
    return re.findall(r'[^\W_]+', plain(value).casefold(), re.UNICODE)[:1000]

def canonical(value):
    try:
        u=urlsplit(str(value)); host=(u.hostname or '').lower()
        if u.scheme not in ('http', 'https') or not host or u.username or u.password:
            return None
        port=u.port
        authority=('['+host+']' if ':' in host else host)
        if port and not ((u.scheme=='https' and port==443) or (u.scheme=='http' and port==80)):
            authority+=':'+str(port)
        query=[(k,v) for k,v in parse_qsl(u.query,keep_blank_values=True) if not k.lower().startswith('utm_') and k.lower() not in TRACKING]
        return urlunsplit((u.scheme,authority,u.path or '/',urlencode(sorted(query)),''))
    except (ValueError,TypeError):
        return None

def _data(result):
    return result.as_dict() if hasattr(result,'as_dict') else dict(result)

def _bm25(query, documents):
    counts=[Counter(doc) for doc in documents];n=len(counts);avg=sum(map(len,documents))/max(n,1) or 1
    df={term:sum(term in count for count in counts) for term in set(query)}
    scores=[]
    for terms,doc in zip(counts,documents):
        score=0.0
        for term in set(query):
            tf=terms[term]
            if tf:
                idf=math.log(1+(n-df[term]+0.5)/(df[term]+0.5))
                score+=idf*tf*2.2/(tf+1.2*(0.25+0.75*len(doc)/avg))
        scores.append(score)
    top=max(scores,default=1) or 1
    return [s/top for s in scores]

def rerank(query, results, lens='balanced'):
    """Return original typed result objects and separate escaped-by-template reasons.

    RRF uses SearXNG's per-result engine membership and positions when available;
    merged ordinal is the documented fallback, never a fabricated source rank.
    Deduplication keys ignore tracking parameters but output URLs are untouched.
    """
    lens=lens if lens in LENSES else 'balanced'
    candidates=[];seen={}
    for ordinal,result in enumerate(list(results)[:300]):
        data=_data(result)
        if any(data.get(k) for k in ('is_ad','sponsored','advertisement','is_sponsored')):
            continue
        key=canonical(data.get('url'))
        if not key:
            continue
        if key in seen:
            # Keep the upstream merged object: provider metadata remains intact.
            continue
        seen[key]=True
        title=tokens(data.get('title'));body=tokens(data.get('content'))
        engines=data.get('engines') or [data.get('engine','unknown')]
        if isinstance(engines,str):engines=[engines]
        engines=set(str(x) for x in engines)
        positions=data.get('positions') or []
        if not isinstance(positions,(list,tuple,set)):positions=[]
        positions=[float(p) for p in positions if isinstance(p,(int,float)) and math.isfinite(p) and p>0]
        ranks=positions or [ordinal+1]*min(len(engines),8)
        rrf=sum(1/(60+p) for p in ranks[:16])
        candidates.append({'item':result,'data':data,'key':key,'ordinal':ordinal,'host':urlsplit(key).hostname,'terms':set(title+body),'doc':title*3+body,'rrf':rrf,'sources':len(engines),'native_positions':bool(positions)})
    q=tokens(query);lexical=_bm25(q,[c['doc'] for c in candidates]);maxrrf=max((c['rrf'] for c in candidates),default=1) or 1
    weights={'balanced':(0.65,0.35,0.13),'research':(0.45,0.55,0.10),'discovery':(0.55,0.45,0.25)}[lens]
    for c,bm in zip(candidates,lexical):c['lexical']=bm;c['score']=weights[0]*c['rrf']/maxrrf+weights[1]*bm
    ordered=[];counts=Counter();remaining=list(candidates)
    while remaining:
        def diversity_score(c):
            similarity=max((len(c['terms']&x['terms'])/max(1,len(c['terms']|x['terms'])) for x in ordered[-20:]),default=0)
            return c['score']-weights[2]*similarity-0.15*counts[c['host']]
        best=max(remaining,key=lambda c:(diversity_score(c),-c['ordinal']))
        remaining.remove(best);ordered.append(best);counts[best['host']]+=1
    explanations={}
    for c in ordered:
        explanations[str(c['data'].get('url'))]={'sources':c['sources'],'text_match':round(c['lexical']*100),'rank_basis':'source positions' if c['native_positions'] else 'merged source order','lens':lens,'version':VERSION}
    return [c['item'] for c in ordered], explanations
