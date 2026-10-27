---
name: crisp-dm-audit
description: Audit a project report for complete, honest coverage of the CRISP-DM methodology (all six phases and 24 generic tasks) and report each gap with a concrete fix. Use this whenever the user asks whether their report covers CRISP-DM, wants their methodology chapter checked or validated, asks "did I miss a phase?" or "is my report complete?", or is about to submit or defend a data-science or machine-learning project report, even if they don't name CRISP-DM.
---

# CRISP-DM coverage audit

The audit has two layers. They catch different failures:

1. **Mechanical check.** Is every one of the 24 generic tasks addressed somewhere, with real prose and no open `[TO VERIFY]` markers? A script answers this in a second.
2. **Examiner's reading.** Does each section actually deliver what its task requires, consistently with the other phases and with the project's real evidence? Only reading catches a "Data Cleaning" section that never says what was cleaned, or business criteria that are never evaluated.

The audit is **read-only** unless the user asks you to fix things. Paths are relative to this skill's base directory. The rubric lives in the sibling skill: `../write-report/references/crisp-dm.md`.

## 1. Locate the report

Usually `report/main.tex` in the project. Then check whether the sources contain `\crispdm{...}` markers (search for `\crispdm`).

- **Markers present** (report written with the write-report skill): continue with step 2.
- **No markers** (the user's own LaTeX report): skip the script. In step 3, map each task to the section that covers it by reading. Afterwards, offer to insert `\crispdm{ID}` markers (plus the macro definitions and the traceability table from `../write-report/assets/report-template/`) so future audits are automatic.
- **PDF or Word report:** extract the text (pdf or docx skill) and do step 3 by reading. Markers don't apply.

## 2. Run the checker

```bash
python scripts/crisp_dm_check.py <report-dir> --strict
```

It follows `\input`/`\include` from `main.tex`, finds every marker, measures the prose of the enclosing section, and reports each task as:

| Status | Meaning |
| --- | --- |
| `OK` | addressed with enough prose |
| `N/A` | declared not applicable (`\crispdm[na]{ID}`) with a justification |
| `UNVERIFIED` | addressed, but the section still contains `\toverify` / `[TO VERIFY` |
| `THIN` | marker present but too little prose (default < 80 words; < 15 for N/A) |
| `MISSING` | no marker anywhere |

Use `--json` when you want to process the result, and `--min-words N` to adjust the threshold. Exit code 1 means there are gaps. The checker can't judge quality, so `OK` only means "addressed and long enough to be worth reading". Step 3 decides whether it's actually good.

## 3. Read each phase like an examiner

For every task, compare the section with the task's **"The report states"** entry in `../write-report/references/crisp-dm.md`. Then check the project evidence (code, data, logs) wherever the report makes a factual claim. Things examiners commonly catch:

- business objectives that are really technical goals ("train a CNN" is not a business objective)
- success criteria defined in Chapter 1 and never evaluated afterwards
- data description numbers that don't match the data, or don't add up to the split sizes
- quality problems found in exploration that cleaning never addresses
- a test design missing, or hyperparameters tuned on the test set
- model metrics reported without a formula or without saying which data split they come from
- evaluation (EV.1) that repeats model metrics without judging them against the business criteria
- deployment described as done when it's only planned
- an N/A without a reason, or a reason that contradicts the evidence

Then check the **golden threads** (consistency links between phases) listed in §3 of `crisp-dm.md`. Each thread either holds or breaks somewhere specific. Say where.

## 4. Report back

Use this shape. Keep it tight, because the user will work through it as a to-do list.

```markdown
## CRISP-DM audit — <report path>

| Phase | Complete | Notes |
| --- | --- | --- |
| Business understanding | 3/4 | BU.3 has no measurable technical success criterion |
| ... | | |

### Fix first (max 5)
1. **EV.1 Evaluate results** (§4.6): repeats the F1 scores from §4.4 but never checks the
   business criterion "reduce manual review time by 50%" (§1.5). Fix: add a paragraph comparing
   the review time measured in <log/file> with that target, or state that it couldn't be measured yet.
2. ...

### Golden threads
- BU.1 → EV.1: broken. Criterion 2 is never evaluated.
- DU.4 → DP.2: holds.
- ...

### Minor
- ...
```

Each fix names the section, the problem, and the concrete content to add or the evidence to use. If the evidence doesn't exist in the project, say so; the fix might be an honest limitation rather than new text. Finish by asking whether to apply the fixes.
