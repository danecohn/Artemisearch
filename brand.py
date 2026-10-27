from pathlib import Path
import shutil
root=Path('/usr/local/searxng/searx');assets=Path('/opt/altstack-search')
base=root/'templates/simple/base.html';text=base.read_text()
text=text.replace('SearXNG — a privacy-respecting, open metasearch engine','Cohnsoft Search — independent web metasearch')
text=text.replace('</head>', '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'altstack.css\') }}"><script defer src="{{ url_for(\'static\', filename=\'altstack-account.js\') }}"></script></head>')
text=text.replace('<body class=', '<body class=',1).replace('<main id=', '<header class="altstack-menubar"><a href="/" class="altstack-brand"><img src="{{ url_for(\'static\', filename=\'img/altstack.svg\') }}" alt="">Cohnsoft Search</a><nav><a href="/office">Office</a><a href="/warehouse">Warehouse</a><a href="/mail">Mail</a><a href="/calendar">Calendar</a><a href="/social">Social</a><a id="search-account" href="/social#account">Your account</a></nav></header><main id=',1)
text=text.replace("{{ _('Powered by') }} <a", "Cohnsoft · {{ _('Powered by') }} <a")
base.write_text(text)
p=root/'templates/simple/index.html';p.write_text(p.read_text().replace('<h1>SearXNG</h1>','<img class="altstack-search-mark" src="{{ url_for(\'static\', filename=\'img/altstack.svg\') }}" alt=""><h1>Cohnsoft Search</h1><p class="altstack-search-note">The whole web. A different perspective.<br>No ads. No paid placements.</p>'))
shutil.copy2(assets/'logo.svg',root/'static/themes/simple/img/altstack.svg')
shutil.copy2(assets/'logo.svg',root/'static/themes/simple/img/favicon.svg')
for name in ['altstack.css','altstack-account.js']:shutil.copy2(assets/name,root/'static/themes/simple'/name)
# Remove the upstream logo in the results search header while preserving search controls.
p=root/'templates/simple/search.html'
if p.exists():p.write_text(p.read_text().replace('SearXNG','Cohnsoft Search'))
# Discard explicitly marked sponsored results if an upstream engine returns any.
p=root/'webapp.py';text=p.read_text();old='results = result_container.get_ordered_results()'
if old not in text:raise RuntimeError('SearXNG result integration changed')
text=text.replace(old,"results = [r for r in result_container.get_ordered_results() if not any((r.as_dict() if hasattr(r, 'as_dict') else r).get(k) for k in ('is_ad', 'sponsored', 'advertisement'))]")
p.write_text(text)

# Modified sources/static assets must not retain upstream precompressed variants.
import base64,re
logo=(assets/'logo.png').read_bytes()
if not logo.startswith(b'\x89PNG\r\n\x1a\n'):raise RuntimeError('Artemis favicon is not a valid PNG export')
for name in ['favicon.png','searxng.png']: (root/'static/themes/simple/img'/name).write_bytes(logo)
for template in (root/'templates/simple').rglob('*.html'):
 text=template.read_text()
 for old in ['img/searxng.png','img/searxng.svg','img/searxng-wordmark.svg']:text=text.replace(old,'img/altstack.svg')
 template.write_text(text)
for path in (root/'static/themes/simple/img').glob('*'):
 if path.suffix in ['.gz','.br'] and any(name in path.name for name in ['favicon','searxng','altstack']):path.unlink()


# Cohnsoft Search additions are applied to the exact pinned upstream image. Fail
# closed during the build if an integration point changes.
for path in [root/'templates/simple/base.html',root/'templates/simple/index.html',root/'templates/simple/search.html']:
    path.write_text(path.read_text().replace('Cohnsoft Search','Cohnsoft Search'))
shutil.copy2(assets/'artemis_ranking.py',root/'artemis_ranking.py')
p=root/'webapp.py';text=p.read_text()
old="results = [r for r in result_container.get_ordered_results() if not any((r.as_dict() if hasattr(r, 'as_dict') else r).get(k) for k in ('is_ad', 'sponsored', 'advertisement'))]"
new="from searx.artemis_ranking import rerank as artemis_rerank\n    results, artemis_explanations = artemis_rerank(search_query.query, result_container.get_ordered_results(), sxng_request.args.get('lens', 'balanced'))"
if text.count(old)!=1:raise RuntimeError('Cohnsoft Search ranking integration changed')
text=text.replace(old,new)
needle='results = results,'
if text.count(needle)!=1:raise RuntimeError('Cohnsoft Search template context integration changed')
text=text.replace(needle,needle+"\n        artemis_explanations=artemis_explanations,\n        artemis_lens=sxng_request.args.get('lens','balanced'),")
p.write_text(text)
p=root/'templates/simple/result_templates/default.html';text=p.read_text()
needle='{{- result_sub_footer(result) -}}'
if needle not in text:raise RuntimeError('Cohnsoft Search result explanation integration changed')
text=text.replace(needle,"""{% if artemis_explanations and artemis_explanations.get(result.url) %}
{% set reason=artemis_explanations[result.url] %}
<details class="artemis-reason"><summary>Why this result?</summary><p>Agreement across {{ reason.sources }} source(s) · Text match {{ reason.text_match }}% within this result set · {{ reason.lens }} lens. Rank fusion uses {{ reason.rank_basis }}. Domain and text diversity reduce repetition. No paid boosts. <a href="https://github.com/danecohn/Artemisearch/blob/main/docs/RANKING.md">How ranking works</a></p></details>
{% endif %}
"""+needle)
p.write_text(text)
p=root/'templates/simple/base.html';text=p.read_text()
text=text.replace('Cohnsoft ·', 'Cohnsoft · <a href="https://github.com/danecohn/Artemisearch">Modified source (AGPL)</a> · <a href="https://github.com/danecohn/Artemisearch/blob/main/ATTRIBUTION.md">Attribution</a> ·')
text=text.replace('<a href="/warehouse">Warehouse</a>','<a href="/warehouse">Cohnsoft Drive</a>')
text=text.replace('</head>', '<script defer src="{{ url_for(\'static\', filename=\'artemisearch.js\') }}"></script></head>')
p.write_text(text)
shutil.copy2(assets/'artemisearch.js',root/'static/themes/simple/artemisearch.js')
p=root/'templates/simple/index.html';text=p.read_text().replace('The whole web. A different perspective.','A clearer view of the web.').replace('No ads. No paid placements.','No ads. No paid placements. Your choice of perspective.');p.write_text(text)
# Never serve stale compressed variants of modified resources.
for path in (root/'static/themes/simple').rglob('*'):
    if path.suffix in ['.gz','.br'] and path.name.split('.')[0] in ['altstack','altstack-account','artemisearch']:path.unlink()
# Replace the result-header wordmark with our own identity; retain upstream credits.
p=root/'templates/simple/search.html';text=p.read_text();needle="{% include 'simple/searxng-wordmark.min.svg' without context %}"
if needle not in text:raise RuntimeError('Search header wordmark integration changed')
text=text.replace(needle,"<img src=\"{{ url_for('static', filename='img/altstack.svg') }}\" alt=\"\"><span class=\"artemis-wordmark\">Cohnsoft Search</span>")
p.write_text(text)
# Wordmark and stylesheet may have upstream precompressed siblings.
for name in ['altstack.css','artemisearch.js']:
    for suffix in ['.gz','.br']:
        path=root/'static/themes/simple'/(name+suffix)
        if path.exists():path.unlink()
# Hashtag query planning happens before provider retrieval; narrow again after it.
shutil.copy2(assets/'artemis_query.py',root/'artemis_query.py')
p=root/'webapp.py';text=p.read_text();needle='    # search\n    search_query = None'
if text.count(needle)!=1:raise RuntimeError('Hashtag query integration changed')
text=text.replace(needle,"    from searx.artemis_query import plan as artemis_plan, narrow as artemis_narrow\n    artemis_query_plan = artemis_plan(sxng_request.form.get('q',''), sxng_request.form)\n    if not artemis_query_plan['effective']:\n        return index_error(output_format, 'Add a search term alongside your filters.'), 400\n\n"+needle)
needle='sxng_request.preferences, sxng_request.form\n        )'
if text.count(needle)!=1:raise RuntimeError('Hashtag provider query integration changed')
text=text.replace(needle,"sxng_request.preferences, artemis_query_plan['form']\n        )")
text=text.replace("artemis_rerank(search_query.query, result_container.get_ordered_results(), sxng_request.args.get('lens', 'balanced'))","artemis_rerank(artemis_query_plan['query']+' '+' '.join(artemis_query_plan['topics']), artemis_narrow(result_container.get_ordered_results(), artemis_query_plan), artemis_query_plan['lens'] or sxng_request.form.get('lens', 'balanced'))")
p.write_text(text)
shutil.copy2(assets/'artemis_ai.py',root/'artemis_ai.py')
p=root/'webapp.py';text=p.read_text();needle="def run():"
if needle not in text:raise RuntimeError('AI route integration changed')
text=text.replace(needle,'from searx.artemis_ai import register as register_artemis_ai\nregister_artemis_ai(app)\n\n'+needle)
p.write_text(text)
shutil.copy2(assets/'artemis-ai.js',root/'static/themes/simple/artemis-ai.js')
p=root/'templates/simple/base.html';text=p.read_text().replace('</head>', '<script defer src="{{ url_for(\'static\', filename=\'artemis-ai.js\') }}"></script></head>');p.write_text(text)

# Cohnsoft canonical identity and local type; keep upstream search behaviour intact.
shutil.copytree(assets/'cohnsoft',root/'static/themes/simple/cohnsoft',dirs_exist_ok=True)
shutil.copy2(assets/'cohnsoft-search.css',root/'static/themes/simple/cohnsoft-search.css')
shutil.copy2(assets/'cohnsoft.js',root/'static/themes/simple/cohnsoft.js')
p=root/'templates/simple/base.html';text=p.read_text()
if '<body class="' not in text:raise RuntimeError('Review Cohnsoft body class integration')
text=text.replace('<body class="','<body class="cs ',1)
links="""<link rel="stylesheet" href="{{ url_for('static', filename='cohnsoft/css/cohnsans.css') }}"><link rel="stylesheet" href="{{ url_for('static', filename='cohnsoft/css/goldengate.css') }}"><link rel="stylesheet" href="{{ url_for('static', filename='cohnsoft-search.css') }}"><script defer src="{{ url_for('static', filename='cohnsoft.js') }}"></script>"""
text=text.replace('</head>',links+'</head>')
for label,new in [('>Office<','>Cohnsoft Office<'),('>Mail<','>Cohnsoft Mail &amp; Calendar<'),('>Calendar<','>Cohnsoft Calendar<'),('>Social<','>Cohnsoft Social<')]:text=text.replace(label,new)
p.write_text(text)
