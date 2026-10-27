# Report notes

Working record for the report: where each claim comes from, what is still missing, and how to rebuild the PDF.

## Sources consulted

| Source (file, log, document, URL) | What it provided |
| --- | --- |
| | |

## Evidence ledger

| Claim made in the report | Evidence (path, test, log, citation) | Confidence (verified / partial / unverified) | Section |
| --- | --- | --- | --- |
| | | | |

## CRISP-DM coverage plan

Status: `covered`, `N/A` (+ reason), or `to verify` (+ what is missing).

| ID | Generic task | Evidence in the project | Status | Section |
| --- | --- | --- | --- | --- |
| BU.1 | Determine business objectives | | | |
| BU.2 | Assess situation | | | |
| BU.3 | Determine data mining goals | | | |
| BU.4 | Produce project plan | | | |
| DU.1 | Collect initial data | | | |
| DU.2 | Describe data | | | |
| DU.3 | Explore data | | | |
| DU.4 | Verify data quality | | | |
| DP.1 | Select data | | | |
| DP.2 | Clean data | | | |
| DP.3 | Construct data | | | |
| DP.4 | Integrate data | | | |
| DP.5 | Format data | | | |
| MO.1 | Select modeling technique | | | |
| MO.2 | Generate test design | | | |
| MO.3 | Build model | | | |
| MO.4 | Assess model | | | |
| EV.1 | Evaluate results | | | |
| EV.2 | Review process | | | |
| EV.3 | Determine next steps | | | |
| DE.1 | Plan deployment | | | |
| DE.2 | Plan monitoring and maintenance | | | |
| DE.3 | Produce final report | This report | covered | General Introduction |
| DE.4 | Review project | | | General Conclusion |

## Open questions for the author

-

## Unverified statements (`\toverify`)

| Section | What is missing | Who or what can confirm it |
| --- | --- | --- |
| | | |

## Numbers and how they were computed

| Value in the report | Command or script that produced it |
| --- | --- |
| | |

## Build

```bash
python <plugin>/skills/write-report/scripts/build_report.py report
python <plugin>/skills/crisp-dm-audit/scripts/crisp_dm_check.py report --strict
```
