from pathlib import Path
import shutil
root=Path('/usr/local/searxng/searx');assets=Path('/opt/altstack-search')
base=root/'templates/simple/base.html';text=base.read_text()
text=text.replace('SearXNG — a privacy-respecting, open metasearch engine','AltStack Search — independent web metasearch')
text=text.replace('</head>', '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'altstack.css\') }}"><script defer src="{{ url_for(\'static\', filename=\'altstack-account.js\') }}"></script></head>')
text=text.replace('<body class=', '<body class=',1).replace('<main id=', '<header class="altstack-menubar"><a href="/" class="altstack-brand"><img src="{{ url_for(\'static\', filename=\'img/altstack.svg\') }}" alt="">AltStack Search</a><nav><a href="/office">Office</a><a href="/warehouse">Warehouse</a><a href="/mail">Mail</a><a href="/calendar">Calendar</a><a href="/social">Social</a><a id="search-account" href="/social#account">Your account</a></nav></header><main id=',1)
text=text.replace("{{ _('Powered by') }} <a", "Artemis Softworks LLC · {{ _('Powered by') }} <a")
base.write_text(text)
p=root/'templates/simple/index.html';p.write_text(p.read_text().replace('<h1>SearXNG</h1>','<img class="altstack-search-mark" src="{{ url_for(\'static\', filename=\'img/altstack.svg\') }}" alt=""><h1>AltStack Search</h1><p class="altstack-search-note">The whole web. A different perspective.<br>No ads. No paid placements.</p>'))
shutil.copy2(assets/'logo.svg',root/'static/themes/simple/img/altstack.svg')
shutil.copy2(assets/'logo.svg',root/'static/themes/simple/img/favicon.svg')
for name in ['altstack.css','altstack-account.js']:shutil.copy2(assets/name,root/'static/themes/simple'/name)
# Remove the upstream logo in the results search header while preserving search controls.
p=root/'templates/simple/search.html'
if p.exists():p.write_text(p.read_text().replace('SearXNG','AltStack Search'))
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


# Artemisearch additions are applied to the exact pinned upstream image. Fail
# closed during the build if an integration point changes.
for path in [root/'templates/simple/base.html',root/'templates/simple/index.html',root/'templates/simple/search.html']:
    path.write_text(path.read_text().replace('AltStack Search','Artemisearch'))
shutil.copy2(assets/'artemis_ranking.py',root/'artemis_ranking.py')
p=root/'webapp.py';text=p.read_text()
old="results = [r for r in result_container.get_ordered_results() if not any((r.as_dict() if hasattr(r, 'as_dict') else r).get(k) for k in ('is_ad', 'sponsored', 'advertisement'))]"
new="from searx.artemis_ranking import rerank as artemis_rerank\n    results, artemis_explanations = artemis_rerank(search_query.query, result_container.get_ordered_results(), sxng_request.args.get('lens', 'balanced'))"
if text.count(old)!=1:raise RuntimeError('Artemisearch ranking integration changed')
text=text.replace(old,new)
needle='results = results,'
if text.count(needle)!=1:raise RuntimeError('Artemisearch template context integration changed')
text=text.replace(needle,needle+"\n        artemis_explanations=artemis_explanations,\n        artemis_lens=sxng_request.args.get('lens','balanced'),")
p.write_text(text)
p=root/'templates/simple/result_templates/default.html';text=p.read_text()
needle='{{- result_sub_footer(result) -}}'
if needle not in text:raise RuntimeError('Artemisearch result explanation integration changed')
text=text.replace(needle,"""{% if artemis_explanations and artemis_explanations.get(result.url) %}
{% set reason=artemis_explanations[result.url] %}
<details class="artemis-reason"><summary>Why this result?</summary><p>Agreement across {{ reason.sources }} source(s) · Text match {{ reason.text_match }}% within this result set · {{ reason.lens }} lens. Rank fusion uses {{ reason.rank_basis }}. Domain and text diversity reduce repetition. No paid boosts. <a href="https://github.com/danecohn/Artemisearch/blob/main/docs/RANKING.md">How ranking works</a></p></details>
{% endif %}
"""+needle)
p.write_text(text)
p=root/'templates/simple/base.html';text=p.read_text()
text=text.replace('Artemis Softworks LLC ·', 'Artemis Softworks LLC · <a href="https://github.com/danecohn/Artemisearch">Modified source (AGPL)</a> · <a href="https://github.com/danecohn/Artemisearch/blob/main/ATTRIBUTION.md">Attribution</a> ·')
text=text.replace('<a href="/warehouse">Warehouse</a>','<a href="/warehouse">Artemis Drive</a>')
text=text.replace('</head>', '<script defer src="{{ url_for(\'static\', filename=\'artemisearch.js\') }}"></script></head>')
p.write_text(text)
shutil.copy2(assets/'artemisearch.js',root/'static/themes/simple/artemisearch.js')
p=root/'templates/simple/index.html';text=p.read_text().replace('The whole web. A different perspective.','A clearer view of the web.').replace('No ads. No paid placements.','No ads. No paid placements. Your choice of perspective.');p.write_text(text)
# Never serve stale compressed variants of modified resources.
for path in (root/'static/themes/simple').rglob('*'):
    if path.suffix in ['.gz','.br'] and path.name.split('.')[0] in ['altstack','altstack-account','artemisearch']:path.unlink()
