# Research Standards

## Source hierarchy (prefer top)
1. Original documents, archives, official records, contemporary reports.
2. Peer-reviewed work, reputable institutional publications.
3. Established journalism with named authors and dates.
4. Encyclopedias and aggregators — as leads to (1)–(3), not as final authority.

## Recording discipline
- Every source: title, author/publisher, origin/URL, publication date, accessed
  date, credibility rating (high/medium/low/unknown), and what it was used for.
- `claims.json` is the single map from statement → evidence. No claim without
  at least one source ID; no source without a use.
- Two independent sources for: surprising claims, statistics, medical/scientific
  results, contested events, quotations.
- Independence means different origin chains, not two sites quoting one wire
  report.

## Conflicts
- Record as conflicts (which sources say what), never silently pick one.
- If unresolved, the script presents the disagreement or drops the claim.

## Numbers
- Record base year, geography, unit, denominator, definition. "Unemployment
  fell" is meaningless without all four.
- Inflation-adjust when comparing money across years; say that you did.

## When web research is unavailable
- State the limitation prominently in `research_report.md`
  (`web_research_available: false`).
- Work only from user-provided material, files on disk, and the agent's
  clearly-labeled background knowledge — mark such claims `UNVERIFIED` unless
  the user can confirm them.
- **Never fabricate sources, URLs, dates, quotes, or statistics.** An invented
  source is a critical integrity failure, worse than an admitted gap.
