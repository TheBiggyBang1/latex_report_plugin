# academic-report: a Claude Code plugin

Writes evidence-based LaTeX academic project reports about the project in your repository and makes sure the methodology covers **all of CRISP-DM**: 6 phases, 24 generic tasks, each traceable to a section of the report.

| Skill | Slash command | What it does |
| --- | --- | --- |
| `write-report` | `/academic-report:write-report` | Explores your repository, asks what the code can't tell, scaffolds `report/`, drafts the chapters, builds `REPORT.pdf` and validates it |
| `crisp-dm-audit` | `/academic-report:crisp-dm-audit` | Checks an existing report for CRISP-DM coverage and lists the gaps with concrete fixes (read-only) |

You don't have to type the slash commands. Saying "write the academic report for this project" or "does my report cover CRISP-DM?" triggers the right skill.

## Install

**1. Requirements**

- Python 3.9 or newer
- A LaTeX distribution with `pdflatex` and `biber`:
  - **MiKTeX** (Windows): https://miktex.org/download. During setup, set *"Install missing packages on-the-fly"* to **Yes**. Otherwise the first build stops at a package-install dialog.
  - or **TeX Live**: https://tug.org/texlive/
- Optional: `pip install pymupdf`, which lets Claude render PDF pages and inspect the layout

Or skip the local install and compile in **Overleaf**: zip the generated `report/` folder, upload it as a new project, and keep the compiler on pdfLaTeX. Overleaf runs biber automatically.

**2. Add the plugin to Claude Code** (from any terminal, on any machine):

```bash
claude plugin marketplace add TheBiggyBang1/latex_report_plugin
```

```bash
claude plugin install academic-report@latex-report-tools
```

Inside an interactive `claude` session, the same thing is `/plugin marketplace add TheBiggyBang1/latex_report_plugin` followed by `/plugin install academic-report@latex-report-tools`. A private repository also works if git on that machine is signed in to GitHub. To try a local clone without installing it:

```bash
claude --plugin-dir ./latex_report_plugin/plugins/academic-report
```

## How CRISP-DM coverage is guaranteed

1. **Markers.** Every section that addresses a CRISP-DM task carries an invisible marker under its heading, e.g. `\crispdm{DU.4}` for *Verify data quality*. A task that truly doesn't apply uses `\crispdm[na]{DP.4}` plus a written reason.
2. **Traceability table.** Chapter 3 contains a table mapping all 24 tasks to "§ 3.4.4, p. 23". It fills itself from the markers, so it never goes stale.
3. **Checker.** `crisp_dm_check.py` reports each task as `OK`, `N/A`, `UNVERIFIED` (still has a `\toverify{...}`), `THIN` (too little prose) or `MISSING`:
   ```bash
   python plugins/academic-report/skills/crisp-dm-audit/scripts/crisp_dm_check.py <project>/report --strict
   ```
4. **Examiner's reading.** The audit skill checks the "golden threads" between phases. For example, every business success criterion from Chapter 1 must be evaluated in Chapter 4, and every data-quality issue must be handled during cleaning.

Where the phases sit by default: Business understanding is Chapter 1; Data understanding, Data preparation and Modeling are Chapter 3; test design, model assessment and Evaluation are Chapter 4; Deployment is planned in Chapter 3; the final report and lessons learned are in the General Introduction and Conclusion.

## Honesty rules built in

The report only states what the repository, data, logs or verified citations support. Anything missing is printed in red as `[TO VERIFY: ...]` and listed in `report/REPORT_NOTES.md`. Results, plots, citations and deployments are never invented. The style and process rules come from `skills/write-report/references/report-guide.md` (your original INSTRUCTIONS.md).

## Layout

```text
.claude-plugin/marketplace.json          local marketplace "latex-report-tools"
plugins/academic-report/
├── .claude-plugin/plugin.json
└── skills/
    ├── write-report/
    │   ├── SKILL.md                     workflow: scaffold → evidence → draft → build → validate
    │   ├── references/report-guide.md   your INSTRUCTIONS.md
    │   ├── references/crisp-dm.md       the 24 tasks, what to write, golden threads
    │   ├── assets/report-template/      main.tex, chapters/, figures/, references.bib, REPORT_NOTES.md
    │   └── scripts/                     scaffold_report.py, build_report.py
    └── crisp-dm-audit/
        ├── SKILL.md
        └── scripts/crisp_dm_check.py
```

## Using the scripts directly

```bash
python plugins/academic-report/skills/write-report/scripts/scaffold_report.py <project>
```

```bash
python plugins/academic-report/skills/write-report/scripts/build_report.py <project>/report
```
