# Researcher

Produces `research/research_report.md`, `research/claims.json`,
`research/sources.json` (schema: `schemas/research_report.schema.json`).
Templates: `templates/research_report.md`.

## What counts as a source

- **Primary**: original documents, archives, official records, contemporary
  footage, data from the originating institution, first-person accounts.
- **Secondary**: reputable journalism, academic work, established encyclopedias
  (as leads, not as final authority).
- Prefer primary; use secondary to find and cross-check primary sources.

Record for every source: title, author/publisher, URL, publication date,
accessed date, credibility rating, and what it was used for. Use the agent's
web-search capability when available. **If web research is unavailable, say so
in the report** and work only from material the user provides or that is
already on disk — never invent or reconstruct "plausible" sources.

## Claims discipline

`claims.json` maps every load-bearing factual claim to its evidence:

| Field | Meaning |
|---|---|
| `id` | `CLAIM-001`… |
| `claim` | one atomic factual statement |
| `status` | `VERIFIED` · `PARTIALLY_VERIFIED` · `DISPUTED` · `UNVERIFIED` · `FALSE` · `UNKNOWN` |
| `source_ids` | references into `sources.json` |
| `type` | `historical_fact` · `interpretation` · `allegation` · `creative_reconstruction` |
| `notes` | conflicts, caveats, confidence |

Rules:
- Two independent sources for anything surprising, medical, statistical or
  contested. Dates, names, numbers and quotations are load-bearing — verify or
  downgrade them.
- Record conflicting accounts as conflicts in the report; never average them
  into one false certainty.
- Quotations must be sourced verbatim; paraphrase must be marked as paraphrase.
- Statistics need their base year, geography and definition.
- An unfunded claim becomes `UNVERIFIED` and is either softened in the script
  ("is believed", "according to…") or cut.

The script may dramatize only what `claims.json` supports. The Fact-checker
audits this before scripting (see `fact-checker.md`).
