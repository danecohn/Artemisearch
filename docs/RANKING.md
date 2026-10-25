# Artemis Rank v1

The engine is ad-free **metasearch**, not yet a new web-scale crawl/index. SearXNG obtains candidates from enabled providers. Provider failures and empty responses are shown by the upstream UI; there is no silent fallback to a different branded search service. Artemisearch reranks at most 300 candidates per response, on that response's page, not across the entire web or every result page.

1. Reject explicitly marked advertisements and non-HTTP(S) or credential-bearing destinations.
2. Deduplicate canonical URL keys without trackers/fragments. Original destination URLs are retained so signature-sensitive URLs are not broken. This is URL deduplication, not a claim to identify every syndicated article.
3. Reciprocal-rank fusion: sum `1/(60 + position)` over upstream source positions. When positions are absent, use the merged upstream ordinal once per source (capped), and label that fallback in the explanation. Provider positions and membership are not necessarily aligned one-to-one by SearXNG.
4. BM25: tokenize visible title/snippet text, title weighted 3×, `k1=1.2`, `b=0.75`. Normalize within the candidate set. It evaluates snippets, not unseen full pages. Unicode words are supported; stemming, learned semantics, and language-specific segmentation are not implemented.
5. Blend fusion and BM25: Balanced 65/35, Research 45/55, Discovery 55/45. These are explicit heuristics, not learned or benchmark-proven optimal weights.
6. Greedy diversification subtracts an overlap penalty (Jaccard text similarity against the last 20 selections) and 0.15 for each already-selected result from the same exact hostname. This reduces repetition without a hidden allowlist, editorial ideology, payment, popularity profile, or demographic inference. Exact hostname is not a registrable-domain classifier; subdomains can remain distinct.

“Why this result?” exposes source count, normalized text match, lens, and the fusion basis. A text-match percentage is relative to this response, **not** a truth score, confidence estimate, or probability. Explanations do not guarantee that a page is safe or accurate.

Lenses travel with the current search request. They are not a user profile. No query history, click feedback, third-party analytics, ads, paid boosts, or AI summary hallucinations are added. Search providers and infrastructure still process requests. Optional existing AltStack account integration stores only explicitly saved search settings, not queries.

## Evaluation

`python3 -m unittest discover -s tests -v` checks ranking invariants and adversarial inputs. `python3 tests/evaluate.py` reports NDCG@5/MRR on a small, clearly labeled **synthetic** relevance set. This is a regression benchmark, not evidence that Artemisearch beats Google, Kagi, or other production search engines. A human-judged, diverse real-query corpus and latency/provider-availability studies are required before making comparative quality claims.

Inspired by the AT Protocol's separation of hosting, AppViews, and feed generators; attribution and algorithm references are in [ATTRIBUTION.md](../ATTRIBUTION.md).

## Hashtag controls

`#research`, `#balanced`, `#discovery` select the ranking lens. `#docs` adds a documentation retrieval term and requires a documentation-related title/snippet/URL. `#opensource` adds “open source” and filters to source-host or explicit open-source text matches; it does not certify a project's license. `#news` selects news, `#day` / `#week` / `#month` / `#year` set the provider time range, `#lang:en` selects a provider language, and `#site:apple.com` restricts exact host/subdomains both at retrieval and after collection. Multiple site tags intersect; disjoint sites yield no results. Ordinary `#topic` tags add quoted retrieval terms and require all their word tokens in the title, snippet, or URL. They can yield fewer or zero candidates. Case folding/Unicode word tokens are supported, not semantic synonyms. C# inside a word is preserved. Provider time/language filters depend on provider support. Active chips show the original controls and remove them explicitly.
