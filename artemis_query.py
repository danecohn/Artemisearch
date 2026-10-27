# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright 2026 VigilTech.
"""Explicit, request-scoped hashtag narrowing. No inferred user profile."""
import re
try:
    from searx.artemis_ranking import plain,tokens
except ImportError:
    from artemis_ranking import plain,tokens
TAG=re.compile(r'(?<!\S)#([\w][\w.-]*(?::[^\s#]+)?)',re.UNICODE)
DOC=re.compile(r'\b(docs?|documentation|manual|reference|guide|developer)\b',re.I)

def plan(raw,form=None):
    raw=str(raw)[:2000];tags=[];topics=[];filters={};lens=None;sites=[];docs=False;opensource=False
    def replace(match):
        nonlocal lens,docs,opensource
        tag=match.group(1);lower=tag.lower();label=None
        if lower in ('balanced','research','discovery'):lens=lower;label='Perspective: '+lower
        elif lower=='docs':docs=True;label='Documentation in title, snippet, or URL'
        elif lower=='opensource':opensource=True;label='Open-source-related title, snippet, or source host'
        elif lower=='news':filters['categories']='news';label='News category'
        elif lower in ('day','week','month','year'):filters['time_range']=lower;label='Time: past '+lower+' (provider filter)'
        elif lower.startswith('site:'):
            host=lower[5:]
            if not re.fullmatch(r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}',host):return match.group(0)
            sites.append(host);label='Only '+host
        elif lower.startswith('lang:'):
            language=lower[5:]
            if not re.fullmatch(r'[a-z]{2,3}(?:-[a-z]{2})?',language):return match.group(0)
            filters['language']=language;label='Language: '+language+' (provider filter)'
        elif ':' in lower:return match.group(0)
        else:topics.append(lower);label='Require topic: '+tag
        tags.append({'tag':'#'+tag,'label':label});return ' '
    query=' '.join(TAG.sub(replace,raw).split())
    effective=query+' '+ ' '.join('"'+topic.replace('"','')+'"' for topic in topics)
    for host in sites:effective+=' site:'+host
    if docs:effective+=' documentation'
    if opensource:effective+=' "open source"'
    effective=effective.strip()
    search_form=dict(form or {});search_form.update(filters);search_form['q']=effective
    # Category checkboxes otherwise override the explicit category string.
    if 'categories' in filters:
        search_form={k:v for k,v in search_form.items() if not k.startswith('category_')}
    return dict(raw=raw,query=query,effective=effective,form=search_form,tags=tags,topics=topics,sites=sites,docs=docs,opensource=opensource,lens=lens)

def narrow(results,query_plan):
    from urllib.parse import urlsplit
    output=[]
    for result in results:
        data=result.as_dict() if hasattr(result,'as_dict') else result
        url=str(data.get('url',''));host=(urlsplit(url).hostname or '').lower();text=plain(str(data.get('title',''))+' '+str(data.get('content',''))+' '+url);words=set(tokens(text))
        if any(not (host==site or host.endswith('.'+site)) for site in query_plan['sites']):continue
        if any(not set(tokens(topic)).issubset(words) for topic in query_plan['topics']):continue
        if query_plan['docs'] and not DOC.search(text):continue
        if query_plan['opensource'] and not (host in ('github.com','gitlab.com','codeberg.org','sr.ht') or re.search(r'\bopen[ -]source\b',text,re.I)):continue
        output.append(result)
    return output
