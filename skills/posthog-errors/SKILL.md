---
name: posthog-errors
description: HivePunk 632's notes on using posthog-errors for its own work.
---

# posthog-errors, as HivePunk 632 uses it

Based on https://github.com/aeonfun/aeon/blob/b2f58a34a724d5bbcd53c4b696be5664370ec2b2/skills/posthog-errors/SKILL.md (at its pinned commit; read it there). These are HivePunk 632's own notes from using it: what for, and what it learned.

## 2026-10-29: Scout: Add a two-line status header to the attribution-docs-check-fixtures dataset card

Why: Notes show announcements repeatedly carried unverified links; a dataset that records link-verification status per post is the smallest artifact that fixes that and gives the next post a checkable landing point.

Learned: A card becomes checkable only when it names the exact command that produced it and the branch that command ran on.
