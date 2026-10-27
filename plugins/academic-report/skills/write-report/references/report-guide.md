# INSTRUCTIONS.md — Recreate a Professional Academic Project Report

> **Purpose:** Use the attached reference report (`watermeters.pdf`) **only as a model for document structure, visual presentation, academic writing conventions, and production workflow**. Create an equally professional report about **the current user's own project**. The water-meter topic, its code, datasets, metrics, claims, and example text are **not** content to reuse.
>
> **Audience:** A coding/writing agent such as Claude Code or OpenAI Codex, working in the user's project repository.
>
> **Important distinction:** The reference PDF was produced with **LaTeX** (verified from its PDF metadata). The sequence below reconstructs a practical way to create a report of this kind; the original author's exact `.tex` sources, prompts, and editing history are not available.

## 1. Mission and deliverables

Study the project supplied by the user, gather verifiable technical evidence, write an academically credible project report, and typeset it with a look and chapter organization inspired by the reference PDF.

**Create:**

1. `report/main.tex` — the main LaTeX document, editable and reproducible.
2. `report/chapters/*.tex` — one source file for each major chapter and front-matter section.
3. `report/figures/` — diagrams, plots, and screenshots actually used.
4. `report/references.bib` — traceable references with complete bibliographic data.
5. `report/REPORT.pdf` — the successfully compiled final report.
6. `report/REPORT_NOTES.md` — a brief record of sources consulted, missing information, unverified statements, and the commands used to build the report.

Do not settle for a Markdown-only report or a PDF that is just a screenshot of text. **The result must be a real, searchable, well-typeset academic PDF, with LaTeX sources.**

If essential project evidence is missing, still produce the best fully honest draft possible, clearly mark `[TO VERIFY: ...]` where necessary, and list outstanding requirements in `REPORT_NOTES.md`. Never invent results merely to complete a section.

## 2. What to reproduce from the reference

The supplied PDF is a **64-page A4 academic report** with a formal serif typesetting style. Use the following as the *design target*, not as rigid rules about page count or subject matter.

| Reference characteristic | Instruction for the new report |
| --- | --- |
| A4 portrait document | Use `a4paper`, a clean text block, and generous academic white space. |
| 12 pt serif body type | Prefer LaTeX's classic Computer Modern / Latin Modern appearance. Use consistent body, heading, and caption fonts. |
| Mostly justified paragraphs | Typeset paragraphs with normal first-line indents, appropriate hyphenation, and comfortable line spacing (approximately 1.4–1.5). |
| Approximately 2 cm left/right text margins | Use balanced margins and leave room for headers, footers, and bound pages; adjust if the institution supplies a template. |
| Bold, large chapter openers | Start each chapter on a fresh page with `Chapter N`, then a large descriptive chapter title, and generous top space. |
| Numbered sections and subsections | Use hierarchical numbers like `3.5`, `3.5.1`, and `3.5.1.1` only as deep as necessary. |
| Running headers | On ordinary content pages, show the current chapter name in small uppercase/italic style at top right, with a thin horizontal line underneath. |
| Centered footer page number | Use consistent automatic page numbering; don't manually type page numbers. |
| Dedicated contents and lists | Generate the Table of Contents, List of Figures, and List of Tables automatically from LaTeX. |
| Numbered figures and tables | Use figure captions **below** images, table captions **above** tables, and labels for cross-references. |
| Plots, workflow diagrams, screenshots | Include clear, relevant visuals with substantive captions; discuss each visual in nearby text. |
| Numbered academic citations | Maintain a bibliography with inline references like `[1]`, `[2]`. Use clickable but subtle source links. |
| Bibliography and webography | Cite papers/books in a bibliography; optionally list websites/tools in a separate webography if required. |

The reference does **not** contain a visible cover page. Do not assume it had one. Add a conventional university/project title page **only if the user or institution requires it**.

**Avoid imitating flaws:** Do not recreate inconsistent claims, repetitive paragraphs, overly long tables, poor caption wrapping, accidental blank space, or references that cannot be verified. Mimic the report's *presentation and reporting logic*, not its imperfections.

## 3. Report architecture

Use the following structure as the default. Adapt terminology to the project, but preserve the distinction between **context**, **related work**, **implementation**, and **measured results**.

```text
Front matter
  [Optional cover page, if explicitly required]
  [Optional dedication]
  [Optional acknowledgements]
  List of Abbreviations
  Abstract and Keywords
  Table of Contents
  List of Figures
  List of Tables

General Introduction

Chapter 1 — Project Overview and Context
  1.1 Introduction
  1.2 Project / Organization Context (only when applicable)
  1.3 General Context and Motivation
  1.4 Problem Statement
  1.5 Project Objectives and Scope
  1.6 Project Plan / Timeline (optional Gantt chart)
  1.7 Conclusion

Chapter 2 — State of the Art
  2.1 Introduction
  2.2 Relevant Research and Existing Approaches
      Literature Review
      Existing Products / Tools / Systems
      Comparative Analysis and Limitations
  2.3 Justification of the Proposed Approach
  2.4 Conclusion

Chapter 3 — Methodology and System Design
  3.1 Introduction
  3.2 Development or Research Methodology
  3.3 End-to-End Workflow / System Architecture
  3.4 Data, Requirements, or Inputs
  3.5 Preparation / Design / Architecture Decisions
  3.6 Implementation and Processing Pipeline
  3.7 Output Format, Validation, and Integration
  3.8 Conclusion

Chapter 4 — Results and Discussion
  4.1 Introduction
  4.2 Experimental Setup / Test Environment
  4.3 Evaluation Criteria and Metrics
  4.4 Functionality and Demonstration Results
  4.5 Quantitative / Qualitative Results
  4.6 Comparisons / Trade-offs (when supported)
  4.7 Error Analysis and Limitations
  4.8 Discussion and Future Improvements
  4.9 Conclusion

General Conclusion and Future Work
Bibliography
[Optional Webography]
[Optional Appendices]
```

### Front matter

- **Dedication and acknowledgements:** Include only with user-supplied names and wording or an explicit request. Never invent people, an internship host, or a supervisor.
- **Abbreviations:** Alphabetize and define only abbreviations genuinely used in the report. Use a two-column abbreviation/meaning layout.
- **Abstract:** Approximately 150–250 words in one or two compact paragraphs. Cover the problem, goal, method, actual implementation, evaluation evidence, conclusion, and limitations. Add 5–10 precise keywords. Write this **last**, after the results are known.
- **Contents, list of figures, list of tables:** Auto-generated, with leader dots and current page numbers. Give preliminary pages Roman numbering where appropriate; restart the main body with Arabic page `1` at the General Introduction.

### General Introduction

Explain the broad field, the concrete real-world problem, why current practices are insufficient, what the project proposes, and how the report is organized. Keep this about the user's project, not generic promotional text.

### Chapter 1 — Overview and context

Answer **why this project exists**. Introduce its use case, constraints, stakeholders, scope, pain points, goals, and success criteria. Include a meaningful Gantt chart or milestone schedule only if reliable dates/tasks are known; otherwise omit it or clearly label it *proposed*.

### Chapter 2 — State of the art

Answer **what others have done and why this solution was chosen**. Examine actual research papers, products, repositories, frameworks, and technical alternatives. For every comparison, explain the evaluation criteria, benefits, trade-offs, and source of each claim. A comparison matrix is useful, but do not fabricate accuracy scores or make universal superiority claims without controlled evidence.

### Chapter 3 — Methodology

Answer **how the project works and how it was built**. This should be the most reproducible chapter:

- Explain the workflow or development framework actually used. Use **CRISP-DM** only when appropriate to a data-driven project; otherwise use a real applicable software engineering, research, design, or experimental process.
- Present a **high-level architecture/workflow diagram** before the implementation details.
- Inventory datasets, assets, inputs, sources, schemas, and constraints with provenance and permissions.
- Explain preparation steps, algorithms, models, modules, services, data flows, storage, APIs, dependencies, and parameters **only when they actually exist in the project**.
- Explain the reasoning behind architectural and engineering choices.
- Include implementation tables, pseudocode, formulas, or code fragments sparingly when they clarify reproducibility.
- Describe outputs and their validation rules, then distinguish completed functionality from proposed integrations.

### Chapter 4 — Results and discussion

Answer **what was demonstrated and how well it worked**. Use screenshots, experiment logs, test reports, benchmark measurements, error examples, and real tables/plots from the actual project. Include:

- Exact environment (hardware, software versions, data/test sets, configuration, dates when relevant).
- Evaluation metrics **with formulas and plain-language definitions**.
- Experiment setup, baselines, and reproducible procedures.
- Actual quantitative results with clearly stated units, datasets, and samples; separate training, validation, and held-out test results where relevant.
- Qualitative demonstrations: interface screenshots, system flow outputs, predictions, and representative successes/failures.
- Limitations, observed errors, validity threats, known failure modes, and realistic improvements.

If the project has no machine-learning training, **do not invent accuracy/loss plots**. For a web, mobile, SaaS, or agent project, replace them with appropriate verified evidence: task success rate, latency, throughput, reliability, accessibility audits, build/test results, user flows, usability findings, cost per run, or traceable feature demonstrations.

### General conclusion

Synthesize the original objectives, what was implemented, what the evidence shows, remaining limitations, and achievable next steps. Do not claim deployment, production readiness, or security guarantees unless they were demonstrated.

## 4. How to gather evidence from MY project

Before writing full prose, inspect the project repository and any documents provided by the user.

**Read-only discovery pass:**

1. Read `README.md`, existing documentation, configuration files, manifests, lockfiles, environment examples, diagrams, and meaningful comments.
2. Inspect the directory structure and identify the implemented entry points, frameworks, data flows, modules, endpoints, infrastructure, and dependencies.
3. Read available tests, benchmark outputs, training logs, notebooks, experiment trackers, or performance reports.
4. Examine representative source files to verify architectural claims. Do not rely on filenames alone.
5. Inspect accessible version-control history and project milestones when helpful. Do not treat commit messages as definitive implementation proof.
6. Identify real images/screenshots/figures and which ones would best explain the system.
7. Identify the missing data required for a credible academic report.

Create a **fact/evidence ledger** for the drafting process:

| Claim to make | Evidence | Confidence | Chapter/figure |
| --- | --- | --- | --- |
| Feature is implemented | Source path, test, or working output | Verified / partial / unverified | Section number |
| Model/API/tool was used | Dependency plus actual invocation | Verified / partial / unverified | Methodology |
| Result achieved | Log, benchmark, test, or dataset | Verified / partial / unverified | Results |
| External fact or comparison | Full citation or credible documentation | Verified / partial / unverified | State of the Art |

Only write **observed facts as facts**. Label expectations, planned work, and estimates explicitly. Mark unverified facts as `[TO VERIFY: description]`, and track them in `REPORT_NOTES.md`.

Never expose `.env` secrets, private API keys, tokens, credentials, private customer information, or sensitive dataset contents in text or figures.

## 5. Figures, charts, tables, and mathematical content

The visual rhythm is important to reproducing the reference style. The reference mixes narrative paragraphs with numbered diagrams, example images, annotated screenshots, training curves, comparison matrices, and tables.

### Required visual-planning pass

Before writing the final LaTeX, propose and then produce only the visuals warranted by the project:

- **Project timeline** — a Gantt or milestone diagram if authentic scheduling data exists.
- **Overall workflow** — a simple box-and-arrow depiction of components and data movement.
- **System architecture** — modules/services, external interfaces, storage, and processing boundaries.
- **Example input / output** — real representative samples, anonymized as needed.
- **Evaluation plots** — generated from actual experiment CSVs/logs or verified records.
- **Comparison tables** — technologies evaluated using clearly defined criteria.
- **Results tables** — metrics, configuration, outcomes, limitations, and trade-offs.

Use vector graphics (PDF, SVG converted to PDF, TikZ, or PGFPlots) for diagrams and plots when possible; use sufficient-resolution PNG/JPEG for screenshots. If a screenshot is a third-party interface, explain and attribute it appropriately. Use consistent grayscale or restrained accent color; do not make a colorful brochure.

**Figure conventions:** center the figure; scale to text width without distorting; put a descriptive numbered caption **beneath** it; insert `\label{fig:...}` and refer to it with `Figure~\ref{fig:...}` in prose. Explain its relevance rather than simply saying “see figure.”

**Table conventions:** put the numbered caption **above** the table; use `\label{tab:...}`; repeat headers on multi-page tables; control column widths and text wrapping; use `booktabs` rules or a similarly restrained bordered style. A long table must remain legible instead of shrinking to illegibility.

**Equations:** use LaTeX math environments, define variables and units, number meaningful equations, and cite formulas adapted from published work when appropriate.

**Never** create synthetic benchmark curves, invented screenshots, fictitious user studies, or unsupported comparison numbers to fill pages.

## 6. Academic writing rules

- Write in clear, formal, technical **English by default**, unless the user specifies another language.
- Prefer third-person academic style or consistent first-person plural, as appropriate. Avoid marketing language and exaggerated claims.
- Each major chapter begins with a short **Introduction** and ends with a **Conclusion** that transitions to the next chapter.
- Use a narrative structure: **problem → rationale → design → implementation → evaluation → limitations**.
- Explain important technical terms at first mention, and define acronyms.
- Keep sections specific to the user's system, not generic descriptions of popular tools.
- Explicitly distinguish **proposed**, **implemented**, **tested**, **deployed**, and **future** functionality.
- Check that all numeric values and configuration settings agree across abstract, body, charts, and conclusion.
- Avoid unsupported language such as “guarantees,” “state-of-the-art,” or “highly accurate” without context.
- Never copy paragraphs, datasets, results, or citations from the example PDF as if they apply to the new project.
- Use original explanations; quote sparingly and cite accurately.
- Ensure headings, figure names, and units use consistent capitalization and terminology.

## 7. Citation and bibliography process

1. Identify which claims require sources: scholarly background, statistics, architecture provenance, product capabilities, and comparisons.
2. Prefer primary research, official documentation, standards, repositories, and original measurements.
3. Verify that each source actually supports its associated claim. Check authors, titles, publication dates, URLs, and access dates for web resources.
4. Create `references.bib` and use `\cite{...}` in LaTeX; select a **numeric citation style** to resemble the reference.
5. Ensure every cited reference appears in the bibliography and every bibliography entry is genuinely used, unless the institution requires further reading.
6. If a separate *Webography* is required, include only relevant actual websites, with access dates as appropriate; do not duplicate or create misleading citations.
7. Attribute diagrams/photos/screenshots sourced elsewhere, including AI-generated artwork if such attribution is required by the user's academic rules.

A polished-looking fake citation is worse than a visibly incomplete citation. Never invent a DOI, publication, title, year, benchmark, or source.

## 8. LaTeX production specification

Use a conventional modular LaTeX project so the user can edit and regenerate the report.

**Recommended directory organization:**

```text
report/
├── main.tex
├── references.bib
├── chapters/
│   ├── abstract.tex
│   ├── abbreviations.tex
│   ├── general_introduction.tex
│   ├── chapter1_context.tex
│   ├── chapter2_state_of_art.tex
│   ├── chapter3_methodology.tex
│   ├── chapter4_results.tex
│   └── general_conclusion.tex
├── figures/
│   ├── workflow.pdf
│   ├── architecture.pdf
│   ├── example_output.png
│   └── ...
├── REPORT_NOTES.md
└── REPORT.pdf
```

**Suggested starting preamble** (adjust to the institution's style requirements):

```latex
\documentclass[12pt,a4paper]{report}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc} % For pdfLaTeX; omit with LuaLaTeX if unneeded
\usepackage{lmodern}
\usepackage[margin=2cm,headheight=16pt,headsep=18pt]{geometry}
\usepackage{setspace}
\setstretch{1.4}
\usepackage{graphicx}
\usepackage{amsmath,amssymb}
\usepackage{booktabs,tabularx,longtable,array}
\usepackage{caption}
\usepackage{float}
\usepackage{fancyhdr}
\usepackage{hyperref}
\usepackage[backend=biber,style=numeric,sorting=none]{biblatex}
\addbibresource{references.bib}

\hypersetup{colorlinks=true,linkcolor=black,citecolor=magenta,urlcolor=magenta}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[R]{\nouppercase{\textit{\leftmark}}}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\fancypagestyle{plain}{%
  \fancyhf{}\fancyfoot[C]{\thepage}%
  \renewcommand{\headrulewidth}{0pt}%
}
```

Notes on fidelity:

- The reference looks like a **classic 12 pt LaTeX `report`-class document**, not a modern magazine or slide deck.
- Chapter headings are large and bold; section headings are smaller and numbered; subsection headings are bold.
- No colorful decorative page backgrounds, full-bleed graphics, oversized icons, or dashboard-style cards.
- Figures and tables belong within the argument and are cited in running text.
- Use unnumbered `\chapter*{...}` for front-matter sections and manually add TOC entries where appropriate.
- Set `\pagenumbering{roman}` for preliminaries and `\pagenumbering{arabic}` at the General Introduction; use `\setcounter{page}{1}` only when necessary.
- Use `\tableofcontents`, `\listoffigures`, and `\listoftables`; recompile enough times for cross-references to resolve.
- Adjust spacing and headers only after inspecting rendered pages, not by guessing from source alone.

Do not claim to reproduce the **exact** LaTeX template or margins: only the PDF is available, so the styling above is a close, editable approximation.

## 9. Step-by-step execution plan for the agent

Follow this order rather than drafting dozens of pages from memory:

**Phase A — Understand:** Explore the user's project and gather its true scope, objective, implementation details, technologies, and available evidence. Preserve a source/evidence ledger.

**Phase B — Plan:** Map authentic project information into the four-chapter structure. Create an outline, list of required figures/tables, citation plan, and a gap list. Remove irrelevant headings rather than forcing unrelated text.

**Phase C — Research:** Look up only the background and comparable approaches actually relevant to the project. Verify each source and save bibliographic metadata. Keep external research distinct from observations about the user's implementation.

**Phase D — Draft:** Write the core Methodology and Results chapters from concrete evidence first; then the State of the Art, Context, Introduction, Conclusion, and finally Abstract. Make cross-chapter claims consistent.

**Phase E — Visualize:** Generate architecture and workflow diagrams from the real implementation. Produce plots from actual measurements. Include real, anonymized screenshots. Add useful captions and labels.

**Phase F — Typeset:** Build the modular LaTeX sources, auto-generated contents/lists, consistent running headers, numbered equations, figures, tables, and citations.

**Phase G — Compile:** Prefer `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` with Biber available for `biblatex`, or an equivalent successful LaTeX build procedure. Fix compilation warnings and broken citations/references before delivery.

**Phase H — Inspect:** Render representative pages and visually audit the PDF, including the front matter, first page of every chapter, dense tables, wide figures, charts, and bibliography. Fix clipping, overflow, poor figure placement, blank pages, bad line breaks, and orphaned headings.

**Phase I — Validate:** Compare the report against the actual repository, test artifacts, and reference list one final time. Generate `REPORT_NOTES.md` with honest limitations and reproducible build instructions.

**Phase J — Deliver:** Provide `REPORT.pdf` and all sources/assets. Briefly summarize what was covered and what is still unverified. Never present `[TO VERIFY]` items as completed facts.

## 10. Completion checklist

Do **not** mark the report finished until all applicable checks pass:

- [ ] Everything is about the user's real project; nothing substantive was copied from the example's topic.
- [ ] The report contains clear context, related work, methodology, results, and conclusions.
- [ ] Each major chapter starts with an introduction and ends with a conclusion.
- [ ] The PDF has consistent A4 typography, whitespace, page numbers, headers, and hierarchy.
- [ ] Contents, figures list, tables list, citations, and cross-references are automatically generated and correct.
- [ ] Every important diagram, plot, screenshot, and table is readable, captioned, and discussed.
- [ ] All technical claims are grounded in inspected project evidence or trustworthy cited sources.
- [ ] Results are real, with test conditions, metrics, and limitations stated precisely.
- [ ] No fictitious papers, citations, benchmarks, institutions, dates, people, or deployments appear.
- [ ] No secrets or personal data are leaked in screenshots, code, or prose.
- [ ] `REPORT.pdf` compiles cleanly and has been inspected visually for layout errors.
- [ ] LaTeX sources and assets are provided so the user can update the report later.
- [ ] Missing information and unresolved issues are listed in `REPORT_NOTES.md`.

## 11. How to invoke these instructions

This is a **reusable instruction document**, not a report about water meters.

- **Claude Code:** In the project folder, say: `Read INSTRUCTIONS.md and create the academic report for this repository. Use the reference PDF only for structure and layout.` To make it part of Claude Code's persistent project instructions, add a short `CLAUDE.md` pointing to this file.
- **Codex:** Say the same in a Codex session, or create an `AGENTS.md` that tells Codex to read and apply `INSTRUCTIONS.md` for report-generation tasks.
- An arbitrary file called `INSTRUCTIONS.md` is **not automatically loaded** by every coding agent. Explicitly reference it, or use that agent's recognized project-instruction file.

**Primary objective: Create the same *category and caliber* of report—an evidence-based, well-structured LaTeX academic project report—adapted completely to the user's own project, not a rewritten copy of the example.**
