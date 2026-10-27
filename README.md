# Vigil Search

Metasearch with no ads and no paid placements.

An open-source search engine by **VigilTech**, founded by **Demetria Althea Cohn**. Built from AltStackSearch and SearXNG with an original, explainable ranking layer and a quiet companion interface for Lookout, macOS, mobile, and any modern browser.

- Reciprocal-rank fusion + BM25 snippet relevance + source/text diversification.
- Balanced, Research, and Discovery perspectives with result explanations.
- No advertising, sponsored ranking, affiliate rewriting, or added query/click tracking.
- macOS system typography, translucent chrome, rounded result cards, accessible touch-sized controls.
- Lookout defaults to Vigil Search; Kagi, DuckDuckGo, and Google remain user choices.
- Served under the existing `/search/` route; no separate domain is needed.

This version is **metasearch**: it depends on upstream providers for candidates. It is not a web-scale independent index or a claim of superior search quality. AT Protocol inspired the architecture; no Bluesky code is reused and no PDS sync/federated ranker is claimed. See [attribution](ATTRIBUTION.md), [ranking and limits](docs/RANKING.md), and [LICENSE](LICENSE).

## Look and contrast

The interface uses the VigilTech Golden Gate design system, copied into `vigiltech/` (Night and Dawn appearances, Vigil Sans, frosted header, pink primary controls). `preview/` holds static pages (search home, results, preferences) for checking the theme without running SearXNG: `python3 -m http.server` from the repository root, then open `/preview/index.html`. They are hand-written markup, not SearXNG output, and are excluded from the Docker image.

## Run

The Dockerfile preserves the baseline's pinned SearXNG image and builds/tests all modifications. Set `SEARXNG_SECRET`, `SEARXNG_BASE_URL`, and authenticated `SEARXNG_VALKEY_URL`; expose `$PORT` (8080 default). Production uses the existing fixed AltStack private proxy; credentials are not forwarded to search. Abuse limiting remains enabled. Health: `/search/healthz` behind the prefix. Keep the corresponding source link visible in the footer.

`python3 -m unittest discover -s tests -v` and `python3 tests/evaluate.py` run without external dependencies. CI builds the pinned container, checks live pages/assets, and exercises the result-rendering integration. The private supplied iCloud archive is not included.

## Product direction

Vigil Search is VigilTech's flagship: an Apple-first alternative for finding information and doing everyday work. Lookout is its native browser companion. Mind, Prompter, VigilTech Drive, Office, and the creative tools form the surrounding software family. This is the product hierarchy, not a claim that every existing app already shares one backend, one subscription, native Swift implementation, or complete cross-app synchronization. Those integrations are developed and documented individually.

## Your perspective, your optional AI

Use `#research`, `#docs`, `#opensource`, `#news`, `#week`, `#site:apple.com`, `#lang:en`, or ordinary topic hashtags to narrow a search. Active controls are visible and removable. [Exact behavior and limits](docs/RANKING.md#hashtag-controls).

AI overviews and follow-up questions are optional and off by default. Bring your own OpenAI or Anthropic API key, choose the model, and explicitly generate a cited answer from the displayed snippets. Keys/conversations are held only in the current page's memory; the server relays requests to fixed provider endpoints without persisting them. Usage is billed to your provider account. [Data flow, privacy, tests, and limits](docs/AI.md).

## Licence and compatibility

This distribution incorporates SearXNG and remains AGPL-3.0-or-later; its upstream LICENSE and source-offer links are preserved. VigilTech-owned brand assets are GPL v3 and Vigil Sans is SIL OFL 1.1. The branding does not change search queries, ranking, hashtags, opt-in AI handling, endpoints or saved account preferences.

A product of VigilTech, vigiltech.org.

Icons: [VigilTech](https://github.com/danecohn/vigilicons), supplied `products/search` kit. Files copied unchanged.
