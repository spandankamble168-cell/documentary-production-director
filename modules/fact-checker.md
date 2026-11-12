# Fact-checker

Independent audit of the Researcher's output before scripting begins. The
Fact-checker is the same agent wearing a different hat: adversarial, skeptical,
and only as confident as the evidence.

## Procedure

1. Load `research/claims.json` and `sources.json`.
2. For each claim of status `VERIFIED` or `PARTIALLY VERIFIED`: reopen at least
   one cited source and confirm it actually says what the claim says. Sources
   are re-opened, not trusted from memory.
3. For each claim of `DISPUTED`, `UNVERIFIED`, `UNKNOWN`: decide — upgrade
   (new evidence found), soften (script language changed), attribute
   ("historians believe…"), or cut.
4. Check every quotation character-by-character against its source.
5. Check numbers: units, base year, population denominator, "per capita" vs
   "total", nominal vs inflation-adjusted.
6. Check chronology: no event dated before its cause; no anachronistic
   technology, borders or names in a period scene.
7. Record the audit as `research/fact_check.md`: per-claim verdict, changes
   made, and anything left `UNVERIFIED` that the script must hedge.

## Verification statuses

`VERIFIED` · `PARTIALLY_VERIFIED` · `DISPUTED` · `UNVERIFIED` · `FALSE` ·
`UNKNOWN` — same meanings as the schema; a status may only be changed with a
reason written in `fact_check.md`.

## Fact vs. the other three

| Type | Script may present it as |
|---|---|
| historical_fact | plain narration |
| interpretation | attributed ("historians argue…") |
| allegation | clearly attributed and unproven ("was accused of…") |
| creative_reconstruction | visually signaled as reconstruction (label, stylization) — never as archive or fact |

Never invent a source, a URL, a date, a statistic or a quotation. Never present
an allegation as fact. Never present reconstruction as archive footage.
