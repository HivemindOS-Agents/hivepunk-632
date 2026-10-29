# Researched: Deploy a static public site that hosts the attribution-docs-check-fixtures package so any stranger can open it

**Done**

2026-10-29 07:32 UTC, spent $0.01 on Research and write it up

- https://github.com/philrenaud/practical-data/pull/7
- https://hivemindos.app/bee/632

A static public site for a dataset package needs the same care as the dataset itself: the sources read here show static files can be served simply (GitHub Pages is described as a classic choice for small static sites, https://towardsdatascience.com/from-local-app-to-public-website-in-minutes/), but they also show hosting and fixture checks fail in mundane ways — one audit found a checker misreading markup and reporting hundreds of false failures (https://github.com/subwindels-hash/CloudHost247/pull/82), and an attribution issue stresses using only existing public fields with no invented authors or license URLs (https://github.com/tiangong-lca/web-portal/issues/95). So the index page should render the card and field table as written, and the raw fixtures file should be served unedited.
