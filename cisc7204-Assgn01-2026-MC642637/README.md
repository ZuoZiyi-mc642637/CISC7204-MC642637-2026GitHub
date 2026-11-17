# Assignment 01 — visitor arrivals and hotel guests in Macao

**CISC7204 · Zuo Ziyi (MC642637) and Member E  · Pair 11.**
**Status:** archived coursework; preliminary proposal. This is separate from the six-person facilities project.

## Research question and evidence
How do monthly visitor arrivals and hotel guest counts relate in Macao, January–June 2026? The analysis joins two six-row tables on month, checks completeness, compares monthly counts and January=100 indices, and calculates Pearson correlation. The supplied table yields r≈0.79. Visitors rise in February and April while hotel guests fall; positive overall association does not imply agreement in every monthly movement.

## Files to inspect
- [Proposal, Notebook, CSVs and three figures](Proposal/)
- [Analysis Notebook](Proposal/CISC7204-Assgn01-MC642637-Proposal_code.ipynb)
- [Monthly counts](Proposal/01_monthly_counts.png)
- [January-based indices](Proposal/02_changes_from_january.png)
- [Correlation view](Proposal/03_correlation.png)
- Module01–06: original Python data-analysis labs and practice/final projects.

## Sources and usage
[DSEC visitor arrivals](https://data.gov.mo/Detail?id=3546225a-2a34-4645-b01e-6752aed03993) and [DSEC hotel guests](https://data.gov.mo/Detail?id=00eae9c4-a51d-4fa2-bd36-7e2db18374a8). The proposal records a 20 September 2026 snapshot. Included CSVs preserve that historical extract; consult publishers for revisions and current reuse conditions. Source ownership remains with the publishers; no general licence is granted for third-party material.

## Reproduce the proposal analysis
From the repository root, install `python -m pip install -r requirements.txt`, then start `python -m jupyterlab`. Open `cisc7204-Assgn01-2026-MC642637/Proposal/CISC7204-Assgn01-MC642637-Proposal_code.ipynb` and select Restart Kernel and Run All Cells. Use its Proposal directory as the working directory; inputs are `visitor_arrivals_2026H1.csv` and `hotel_guests_2026H1.csv`. The original notebooks are preserved. This guide covers the proposal analysis, not every module's separate environment.

## Limitations and contribution
Six monthly observations cannot support forecasting or causal inference. Visitor and hotel-guest counts represent different populations and do not link individual visitors to hotels. The source notebooks and proposals should be read alongside the figures.

The proposal assigns Zuo Ziyi coordination, source-file organisation, data checking and the first line chart; Member E records analysis steps, develops correlation analysis and drafts interpretation. Both review the outputs. Assignment 02 revises the same tourism study rather than supplying an independent dataset.

## Learning and visual communication
I learned to align two tables by month and distinguish absolute scale from relative change. Counts show magnitude; January=100 indices enable comparison of relative movement; scatterplots summarise association. Labels, units, the short observation period and non-causal wording are essential to interpreting the charts.

Original coursework files and their authorship remain unchanged. Broader module notebooks are archived, not newly certified by this portfolio update.
