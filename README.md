# Artemisearch

**A clearer view of the web. No ads. No paid placements.**

An open-source search engine by **Artemis Softworks LLC**, founded by **Demetria Althea Cohn**. Built from AltStackSearch and SearXNG with an original, explainable ranking layer and a quiet companion interface for Lookout, macOS, mobile, and any modern browser.

- Reciprocal-rank fusion + BM25 snippet relevance + source/text diversification.
- Balanced, Research, and Discovery perspectives with result explanations.
- No advertising, sponsored ranking, affiliate rewriting, or added query/click tracking.
- macOS system typography, translucent chrome, rounded result cards, accessible touch-sized controls.
- Lookout defaults to Artemisearch; Kagi, DuckDuckGo, and Google remain user choices.
- No domain needed: initially served through the existing AltStack `/search/` route.

This version is **metasearch**: it depends on upstream providers for candidates. It is not a web-scale independent index or a claim of superior search quality. AT Protocol inspired the architecture; no Bluesky code is reused and no PDS sync/federated ranker is claimed. See [attribution](ATTRIBUTION.md), [ranking and limits](docs/RANKING.md), and [LICENSE](LICENSE).

## Run

The Dockerfile preserves the baseline's pinned SearXNG image and builds/tests all modifications. Set `SEARXNG_SECRET`, `SEARXNG_BASE_URL`, and authenticated `SEARXNG_VALKEY_URL`; expose `$PORT` (8080 default). Production uses the existing fixed AltStack private proxy; credentials are not forwarded to search. Abuse limiting remains enabled. Health: `/search/healthz` behind the prefix. Keep the corresponding source link visible in the footer.

`python3 -m unittest discover -s tests -v` and `python3 tests/evaluate.py` run without external dependencies. CI builds the pinned container, checks live pages/assets, and exercises the result-rendering integration. The private supplied iCloud archive is not included.
