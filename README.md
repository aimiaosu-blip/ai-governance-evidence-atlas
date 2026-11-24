# AI Governance Evidence Atlas

A small, reproducible research portfolio for comparing governance concepts and drafting traceable policy synthesis. Built with Codex assistance for an AI governance research application. Independent work; no UN ODET affiliation or commissioned research is claimed.

## Read the research

- [Policy brief](docs/policy-brief.md): a proposed documentation pilot and three questions for consultation.
- [Evidence crosswalk](docs/crosswalk.md): nine curated statements linked to three official sources and exact sections.
- [Concept map](docs/concept-map.md): source-to-claim-to-inference lineage.
- [Consultation protocol](docs/consultation-protocol.md): workshop preparation and a dissent-preserving synthesis template.
- [Scope and research decisions](docs/methodology.md).

## Run locally

Python 3.10+; standard library only. No model API, API key or packages needed.

```sh
python -m unittest discover -s tests -v
python atlas.py
```

The script checks referential integrity and rebuilds the crosswalk (Markdown and CSV), policy brief and Mermaid concept map. Tests deliberately break citations, labels and reviewer attribution. They validate data structure, not the truth of policy interpretations.

## What this demonstrates

Primary-source selection, provision-level evidence records, neutral synthesis, explicit separation of source summaries and analyst inferences, visual lineage and reproducible document production. The corpus uses OECD's May 2024 principles update, UNESCO's 2021 Recommendation and the adopted 2024 Global Digital Compact.

## What remains open

Independent human review is pending. No interviews, Delphi exercise or expert consensus have been conducted. National/regional instruments and implementation evidence are outside this first sample. The selected texts do not establish that jurisdictions have equivalent legal duties. This portfolio does not make compliance determinations or claim a current exhaustive legal survey.
