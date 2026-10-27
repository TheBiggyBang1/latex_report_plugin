---
name: write-report
description: Write or update an evidence-based academic project report in LaTeX (report/main.tex, one file per chapter, references.bib, compiled REPORT.pdf) about the project in the current repository, with full CRISP-DM methodology coverage for data-science and machine-learning projects. Use this whenever the user wants to write, draft, structure, extend, fix or finish a university, internship, capstone, PFE / end-of-studies or thesis-style project report ("rapport"), wants LaTeX to document their project, or asks to document a data/ML project with CRISP-DM, even if they don't mention LaTeX.
---

# Write an academic project report

Produce a real, searchable, well-typeset academic report about the user's own project, grounded in evidence from their repository. For data-driven projects, the methodology follows CRISP-DM and every one of its 24 generic tasks is traceable to a section of the report.

Paths in this file are relative to this skill's base directory. The sibling skill `crisp-dm-audit` lives in `../crisp-dm-audit/`.

## What you deliver (in the user's project)

```text
report/
├── main.tex, chapters/*.tex, figures/, references.bib   editable sources
├── REPORT.pdf        compiled, searchable PDF
└── REPORT_NOTES.md   sources, evidence ledger, CRISP-DM coverage plan, gaps, build commands
```

## Ground rules

The report is graded and usually defended in front of a jury, so every sentence has to survive the question "how do you know?". These rules follow from that:

- **Facts come from evidence.** Write as fact only what you observed in the code, data, logs, tests or a cited source. Record each important claim in the evidence ledger in `REPORT_NOTES.md`.
- **Gaps stay visible.** When something can't be verified, write `\toverify{what is missing}` (it prints in red) and list it in `REPORT_NOTES.md`. An honest red marker is better than a polished invention, because the student has to defend every number.
- **Never fabricate** results, plots, screenshots, user studies, citations, DOIs, dates, people, institutions or deployments. If the project has no ML training, don't produce accuracy curves. Use the evidence that does exist instead.
- **Status words are precise.** Keep *proposed*, *implemented*, *tested*, *deployed* and *future* distinct. CRISP-DM's deployment phase is often only planned in student projects, so say that plainly.
- **No secrets.** Never copy `.env` values, keys, tokens, credentials or personal data into text or figures.

`references/report-guide.md` is the full style and process guide: design targets, chapter architecture, figure, table and citation conventions, and the completion checklist (§10). Read §2–§8 before drafting. It mentions a reference PDF (`watermeters.pdf`). That PDF isn't bundled; its layout is already built into the template.

## Workflow

### 1. Scaffold the LaTeX project

```bash
python scripts/scaffold_report.py <project-root>
```

This copies `assets/report-template/` into `<project-root>/report/` and never overwrites existing files. If the user already has a report or an institutional template, don't scaffold over it. Port the CRISP-DM pieces into their template instead: the `\crispdm`, `\crisploc` and `\toverify` macros from the template's `main.tex` preamble, `chapters/crisp_dm_matrix.tex`, `figures/crisp_dm_cycle.tex`, and the CRISP-DM entries of `references.bib`. Institutional formatting rules (cover page, margins, language) override this template's style.

### 2. Understand the project (read-only)

Do the discovery pass from guide §4: README, docs, configs, dependency manifests, source entry points, tests, notebooks and logs. Read representative source files instead of trusting filenames. For a CRISP-DM report, look for evidence of each phase:

| Phase | Where the evidence usually is |
| --- | --- |
| Business understanding | README, project brief, specification, supervisor's subject. Often only the user knows, so ask. |
| Data understanding | `data/` folders, dataset cards, download scripts, EDA notebooks |
| Data preparation | preprocessing and augmentation code, cleaning notebooks, config files |
| Modeling | training scripts, model definitions, hyperparameter configs (YAML/JSON), checkpoints |
| Evaluation | evaluation scripts, metric logs (CSV/JSON, TensorBoard, W&B, MLflow), confusion matrices |
| Deployment | API or app code, Dockerfiles, model export (ONNX/TFLite), CI pipelines |

Git history (if present) helps date milestones and show real iterations between phases. Treat commit messages as hints, not proof.

### 3. Ask the user what the repository cannot tell you

After discovery, ask **one** batch of short questions (about 8 at most). Ask only for what you couldn't find:

- business context: who has the problem, what it costs today, host organization (if any)
- business success criteria, and whether technical thresholds (e.g. a target F1 score) were fixed *before* the experiments
- real timeline and milestones (for the project plan or Gantt chart)
- deployment status: running somewhere, prototype only, or planned
- institution requirements: language, cover page, page limit, citation style
- names for acknowledgements or the title page, but only if the user wants those sections

Don't block on the answers. Draft with `\toverify{...}` for anything still open.

### 4. Plan CRISP-DM coverage

Read `references/crisp-dm.md`. It defines the 24 generic tasks, what each section must contain, where each task sits in the report, and the consistency checks ("golden threads") between phases. Then fill the **CRISP-DM coverage plan** table in `REPORT_NOTES.md`: for every task, note the evidence found, or *N/A + reason*, or *to verify*, plus the target section. Then outline the figures, tables and citations you need.

If the project isn't data-driven, CRISP-DM doesn't fit (see "When CRISP-DM does not fit" in `references/crisp-dm.md`). Tell the user, and use an applicable methodology rather than forcing the phases onto it.

### 5. Draft

Write in this order: Chapter 3 (Methodology) and Chapter 4 (Results) first, from evidence; then Chapter 2 (State of the Art), Chapter 1 (Context), General Introduction, General Conclusion, and the Abstract **last**. Writing the evidence-heavy chapters first keeps the framing chapters honest about what was achieved.

Handling the CRISP-DM markers:

- Each template section that addresses a CRISP-DM task carries an invisible marker such as `\crispdm{DU.4}` right under its heading. The markers feed the traceability table and the coverage checker. Keep each marker under the heading of the section that addresses its task, and move it if you restructure. Merging several tasks into one section is fine: put all their markers there.
- A task that genuinely doesn't apply gets `\crispdm[na]{DP.4}` plus one to three sentences explaining why (e.g. "all data came from a single source, so no integration was needed"). Silence is not N/A.
- Replace the template's `%` guidance comments with prose as you go, and delete the comments you've handled.
- Compute numbers (dataset sizes, class counts, split sizes, metrics) with a script run on the real data and logs, never from memory. Record the command in `REPORT_NOTES.md` so the figures can be regenerated.
- Describe the iterations that actually happened (e.g. weak recall in model assessment sent you back to data preparation). CRISP-DM is a cycle, and real back-loops make the methodology credible. Don't invent loops that didn't happen.

Writing style follows guide §6: formal technical English unless the user asks for another language, chapters that open with an Introduction and close with a Conclusion, acronyms defined at first use, and no marketing language.

### 6. Figures and tables

Follow guide §5. The template already contains the CRISP-DM cycle diagram (`figures/crisp_dm_cycle.tex`, TikZ) and the traceability table (`chapters/crisp_dm_matrix.tex`), which fills itself in from the markers. Draw architecture and workflow diagrams from the real implementation. Generate plots with matplotlib from real logs, saved as PDF into `report/figures/`, and keep the plotting script in the project. Captions go below figures and above tables. Discuss every visual in the text.

### 7. Build

```bash
python scripts/build_report.py <project-root>/report
```

This runs pdflatex → biber → pdflatex (repeated until references settle), copies `main.pdf` to `REPORT.pdf`, and lists undefined references, undefined citations, duplicate labels and overfull boxes. It doesn't need Perl or latexmk. If no TeX distribution is installed, the script says so. Ask whether the user compiles elsewhere (Overleaf: zip `report/`, upload it, keep pdfLaTeX, and biber runs automatically) or wants to install MiKTeX or TeX Live (see the plugin README). Never skip the build silently. When the user compiles in Overleaf, ask for the PDF back for steps 8–9, or for the log's warnings. Fix every error, undefined reference and undefined citation before moving on.

### 8. Inspect the rendered pages

Render pages to PNG and look at them, because layout problems are invisible in the source:

```bash
python -c "import fitz,sys; d=fitz.open(sys.argv[1]); [d[i].get_pixmap(dpi=70).save(f'{sys.argv[2]}/page-{i+1:03d}.png') for i in range(len(d))]" report/REPORT.pdf <scratch-dir>
```

(`pip install pymupdf` if needed.) Check the front matter, every chapter opener, the traceability table, dense tables, wide figures and the bibliography. Fix clipping, overflow, floats drifting far from their discussion, blank pages and orphaned headings.

### 9. Validate

1. Run the coverage checker in strict mode. It must pass:
   ```bash
   python ../crisp-dm-audit/scripts/crisp_dm_check.py <project-root>/report --strict
   ```
2. Do the reviewer-style reading described in `../crisp-dm-audit/SKILL.md` (step 3). Above all, check the golden threads: each business success criterion is evaluated in EV.1, each data-quality issue is handled in DP.2, and the test design matches the reported results.
3. Go through guide §10 (completion checklist) against the actual repository and the reference list.

`--strict` fails while any `\toverify` remains inside a CRISP-DM section. When the user still owes information, deliver anyway and say clearly which items are open. Don't delete the markers to make the check pass.

### 10. Deliver

Tell the user, briefly:
- where `REPORT.pdf` and the sources are
- CRISP-DM coverage per phase (from the checker)
- every `\toverify` item still open and what information would close it
- anything you could not do (e.g. no LaTeX installed, so not compiled)

## Reference files

| File | Read it when |
| --- | --- |
| `references/report-guide.md` | Before drafting (§2–§8), and at the end (§10 checklist) |
| `references/crisp-dm.md` | Planning coverage (step 4), and while writing each CRISP-DM section |
| `assets/report-template/` | Scaffolded by step 1. Read `main.tex` and the chapter files for guidance comments. |
| `scripts/scaffold_report.py`, `scripts/build_report.py` | Steps 1 and 7 |
