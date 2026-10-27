# Attribution and open-source foundations

Cohnsoft Search is produced by **Cohnsoft**, founded by **Demetria Althea Cohn**. Original modifications, ranking code, and interface: © 2026 Cohnsoft, AGPL-3.0-or-later. No warranty; see LICENSE. Corresponding modified source is available at https://github.com/danecohn/Artemisearch .

## Reused software

- **AltStackSearch**, https://github.com/danecohn/AltStackSearch , baseline commit `784bd325f1a78c3a1656d3491a27ffa404da9e04`: deployment configuration, SearXNG branding patches, account-preference integration, ad filtering. AGPL-3.0-or-later. Original notices and LICENSE are retained.
- **SearXNG**, https://github.com/searxng/searxng : metasearch, result collection, engine adapters, privacy controls, and abuse limiter. AGPL-3.0-or-later and the upstream component notices. The Dockerfile retains the exact baseline image digest. The image's OCI source/revision labels identify its corresponding upstream source. The build applies all modifications from this public repository; it does not rename upstream work as original software.

## Architectural inspiration, not copied code or an affiliation

**AT Protocol and Bluesky**, https://atproto.com/guides/overview and https://github.com/bluesky-social/feed-generator : separation of data hosting, indexing/application views, and user-selected feed algorithms inspired Cohnsoft Search's separation of source adapters, ranking, and selectable perspectives. A PDS is a Personal Data Server, not a search-ranking algorithm. No Bluesky/PDS code is copied into this version. Cohnsoft Search is not an AT Protocol implementation, a Bluesky service, or endorsed by Bluesky. Account/PDS synchronization and third-party ranker federation are not implemented in v1.

## Published information retrieval algorithms

Original Python implementations adapt these published methods; they do not copy a package implementation:

- Cormack, Clarke, and Büttcher, **Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods**, SIGIR 2009, https://doi.org/10.1145/1571941.1572114 .
- Robertson and Zaragoza, **The Probabilistic Relevance Framework: BM25 and Beyond**, 2009, https://doi.org/10.1561/1500000019 .
- Carbonell and Goldstein, **The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries**, SIGIR 1998, https://doi.org/10.1145/290941.291025 . Our diversity penalty is inspired by MMR, not an exact implementation of that paper.

Search results and snippets belong to their respective publishers. Provider availability and terms vary. No ads, paid placements, paid ranking, or affiliate link rewriting are added by Cohnsoft Search. Explicitly labeled upstream sponsored candidates are discarded; unlabeled advertising cannot be guaranteed detectable by this filter.
