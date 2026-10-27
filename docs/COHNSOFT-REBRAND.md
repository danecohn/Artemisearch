# Cohnsoft Search

Production source: Artemisearch main (baseline 8f4bbd91b2ad8cc263d618373f320af3140dbc76), behind the existing /search proxy. Name, homepage/result wordmark, settings, optional AI notices, publisher labels and first-party documentation become Cohnsoft Search. Canonical assets/local fonts are pinned to cohnsoftassets@752e894f90f1e58e62ae466352cb03c8bfd7d703 with SHA-256 provenance. Golden Gate controls support light/dark, reduced motion/transparency and visible focus.

No change to module names, static compatibility URLs, cookies, account-preference storage keys, private proxy route, environment names, query/ranking logic, provider endpoints or API-key handling. SearXNG, AT Protocol/Bluesky and other upstream notices are retained. AI remains opt-in and off by default.

32 tests pass for ranking, hashtag narrowing and AI boundaries. Synthetic regression benchmark remains mean NDCG@5 0.9861 / MRR 1.0; this is not a comparative quality claim. The pinned Docker build applies and validates the real upstream integration; production browser/search checks follow deployment.
