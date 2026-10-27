# Running the upstream audit

The GitHub Actions workflow **Audit upstream BattleScribe data** retrieves the selected 3rd, 4th, 5th and 7th Edition repositories and the historical 6th Edition release in a temporary GitHub runner. It then generates `build/audit.json`.

Run from **Actions → Audit upstream BattleScribe data → Run workflow** or push a change to the tools or sources directories.

Download the **middlehammer-upstream-audit** artifact from the completed workflow run to inspect results. Downloaded source archives are **not committed to the public repository** and are not uploaded as artifacts.

A successful workflow proves only that the files can be downloaded and parsed. It does not prove that references resolve, that all original codexes are accurate, or that New Recruit can import the combined data. These require subsequent validation.

**Important:** The current source manifest tracks branch names, not pinned immutable commit SHAs. Before publishing converted catalogues, pin each source to a specific commit, review redistribution permissions, and test in New Recruit.
