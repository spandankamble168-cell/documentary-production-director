# Fact-checking Standards

## Statuses and what they permit
| Status | Meaning | Script treatment |
|---|---|---|
| VERIFIED | ≥1 primary or ≥2 independent credible sources, checked directly | plain statement |
| PARTIALLY_VERIFIED | core holds, details uncertain | plain statement of the core, hedge the details |
| DISPUTED | credible sources disagree | present as dispute, attribute both sides |
| UNVERIFIED | plausible, no adequate source | hedge hard or cut; never plain |
| FALSE | contradicted by evidence | must not appear; note why in fact_check.md |
| UNKNOWN | cannot be established | omit or frame explicitly as open question |

## Checks (every load-bearing claim)
1. **Source says what we claim.** Re-open the source; confirm the claim is not
   an overreach of it.
2. **Quotations verbatim.** Character-exact or marked as paraphrase.
3. **Numbers**: unit, year, geography, denominator, adjustment.
4. **Chronology**: causes precede effects; no anachronism in period scenes.
5. **Names**: spelling, titles at the time, transliteration consistency.
6. **Causation vs correlation**: the script should not assert causality the
   sources don't.
7. **Living people / allegations**: attribute, mark unproven, defamation-aware
   phrasing.

## Four registers (never blur them)
- **historical fact** → narrate plainly.
- **interpretation** → "historians argue", "the consensus is".
- **allegation** → "was accused of", "allegedly", never as established.
- **creative reconstruction** → visually labeled; never passed as archive.

## Output
`research/fact_check.md`: per-claim verdict, edits made, remaining UNVERIFIED
items that the script must hedge. A claim's status changes only with a written
reason there.
