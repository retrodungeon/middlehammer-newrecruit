# Unification Patch v1.7.2 — rules implementation ledger

Source: **The Book of the Unification**, version 1.7.2, connected Google Drive document. The patch uses 5th Edition as its baseline and permits codexes from 3rd through 7th editions.

## Implemented experimentally in root game system

- Standard 5th Edition Force Organization Chart slot bounds: HQ 1–2; Troops 2–6; Elites 0–3; Fast Attack 0–3; Heavy Support 0–3.
- These are *roster validation constraints* only. Confirm New Recruit correctly enforces them; do not infer success from XML alone.

## Extracted patch rules — not yet encoded

- For publications lacking a normal force organization chart, standard 5th Edition chart is available.
- Formations are disallowed.
- Detachment command benefits are ignored.
- Warlord traits are not used.
- Warp charge mechanics are not used.
- Allies are limited to codexes within 3rd–5th or 6th–7th edition groupings, respectively.
- Super-heavy units are disallowed at **1500 points or below**, unless both players agree. Above 1500 points, additional faction-specific allowances and conditions apply.
- 2+ invulnerable saves cannot be improved beyond 3+; natural 1 fails, and a 2+ invulnerable save cannot be rerolled.
- 6th/7th edition hull points are not used.

## Important caveats

The published root catalogues still contain **placeholder units and placeholder costs**. Do not treat them as codex-accurate. The earlier generated Imperial Guard and Chaos Space Marines source conversions exist only in GitHub Actions artifacts pending redistribution review. Rules requiring codex-specific flags or selections cannot be enforced meaningfully until real units are integrated.

Next hands-on test: import/update the repository in New Recruit, make an empty list and verify it reports missing 1 HQ and 2 Troops; add 2 Troops and verify HQ is still required; add a third HQ (requires future real or original test HQ entry) and verify maximum 2.
