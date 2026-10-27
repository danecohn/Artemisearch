# Vigil Search rebrand

VigilTech company labels, Vigil Search product name, supplied lamp artwork and local Vigil Sans replace the previous identity. Shared Golden Gate styles and a narrow Search bridge implement Night/Dawn/System appearance, a system-font switch, pink controls/links, 44px phone targets, reduced motion/transparency and forced colors. The old presentation-only Moonrise artwork is removed.

Canonical assets are copied byte-for-byte from cohnsoftassets@30186592391b296d788f29b411d5701ef4f972e3 with SHA256 provenance. No artwork was invented. Legacy saved preference keys are read for migration; all new appearance writes use VigilTech keys. Backend module names, /artemis/overview API, ranking/query logic, account keys and upstream notices remain compatible. Private Railway service DNS is unchanged.

This distribution remains AGPL-3.0-or-later because SearXNG requires it. Its original LICENSE/source offer are preserved. New brand assets carry their GPL licence, and Vigil Sans carries SIL OFL. Relabelling the combined distribution GPL-only would be incorrect.

32 ranking/hashtag/AI boundary tests pass. The four-query synthetic regression is unchanged (mean NDCG@5 0.9861, MRR 1.0), not a comparative quality claim. The branding patch applies to the exact upstream revision identified by the pinned Docker digest. Real local Flask/WebKit checks are recorded in the PR. Local preview alone disables abuse limiting because it has no Valkey; production settings keep limiter true and the authenticated production Valkey URL unchanged. No paid AI provider calls were made.
