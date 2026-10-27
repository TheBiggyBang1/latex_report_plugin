# CRISP-DM reference for academic project reports

CRISP-DM (Cross-Industry Standard Process for Data Mining) organizes a data project into six phases and 24 generic tasks, each with defined outputs. The source is the CRISP-DM 1.0 guide (`chapman2000crisp` in the template's `references.bib`). This file turns those tasks into concrete expectations for a student report.

Contents:
1. Where each task lives in the report
2. The 24 tasks: what the report states, where the evidence is, common pitfalls
3. Golden threads: consistency checks across phases
4. Presenting CRISP-DM honestly: iterations, N/A tasks, deployment status
5. Citing CRISP-DM and its alternatives
6. When CRISP-DM does not fit

---

## 1. Where each task lives in the report

The template places the markers like this. Moving a task elsewhere is fine as long as its `\crispdm{ID}` marker moves with it. The traceability table updates itself.

| Phase | ID | Generic task | Template location |
| --- | --- | --- | --- |
| Business understanding | BU.1 | Determine business objectives | Ch. 1, Business Objectives and Success Criteria |
| | BU.2 | Assess situation | Ch. 1, Situation Assessment |
| | BU.3 | Determine data mining goals | Ch. 1, Data Mining Goals and Success Criteria |
| | BU.4 | Produce project plan | Ch. 1, Project Plan (tool choices are justified in Ch. 2) |
| Data understanding | DU.1 | Collect initial data | Ch. 3, Data Understanding |
| | DU.2 | Describe data | Ch. 3, Data Understanding |
| | DU.3 | Explore data | Ch. 3, Data Understanding |
| | DU.4 | Verify data quality | Ch. 3, Data Understanding |
| Data preparation | DP.1 | Select data | Ch. 3, Data Preparation |
| | DP.2 | Clean data | Ch. 3, Data Preparation |
| | DP.3 | Construct data | Ch. 3, Data Preparation |
| | DP.4 | Integrate data | Ch. 3, Data Preparation |
| | DP.5 | Format data | Ch. 3, Data Preparation |
| Modeling | MO.1 | Select modeling technique | Ch. 3, Modeling |
| | MO.2 | Generate test design | Ch. 4, Experimental Setup and Test Design |
| | MO.3 | Build model | Ch. 3, Modeling |
| | MO.4 | Assess model | Ch. 4, Model Assessment |
| Evaluation | EV.1 | Evaluate results | Ch. 4, Evaluation Against Business Success Criteria |
| | EV.2 | Review process | Ch. 4, Review of the Process |
| | EV.3 | Determine next steps | Ch. 4, Discussion and Next Steps |
| Deployment | DE.1 | Plan deployment | Ch. 3, Deployment and Integration |
| | DE.2 | Plan monitoring and maintenance | Ch. 3, Deployment and Integration |
| | DE.3 | Produce final report | General Introduction (this report is the deliverable) |
| | DE.4 | Review project | General Conclusion, Lessons Learned |

Why MO.2 and MO.4 sit in Chapter 4: the report guide puts the experimental setup and measured results in the Results chapter. Chapter 3's Modeling section should point forward to them. If the deployment decision followed the evaluation, DE.1 and DE.2 can move to the end of Chapter 4.

---

## 2. The 24 tasks

Each entry lists the official CRISP-DM outputs, what the report must state, where to look in a repository, and the pitfalls examiners notice.

### Phase 1: Business understanding

Business understanding is mostly *not* in the code. Expect to ask the user for it (write-report skill, step 3).

**BU.1 Determine business objectives.** Outputs: background, business objectives, business success criteria.
- *The report states:* who has the problem and how it is handled today; what that costs (time, money, errors, risk); the objective in business terms; and **measurable business success criteria** (e.g. "halve the time analysts spend on manual review", "flag defective items before shipping").
- *Evidence:* project brief, README, supervisor's subject, the user's answers.
- *Pitfalls:* technical goals posing as business goals ("build a YOLO model"); criteria that can never be checked; criteria that Chapter 4 never mentions again.

**BU.2 Assess situation.** Outputs: inventory of resources; requirements, assumptions and constraints; risks and contingencies; terminology; costs and benefits.
- *The report states:* the people, data, hardware and software available; constraints (deadline, privacy or legal rules, compute limits, data access); a short risk table with mitigations; domain terms (which also feed the List of Abbreviations); costs and benefits, described qualitatively when no figures exist.
- *Evidence:* `requirements.txt`/`environment.yml`, hardware mentioned in logs or notebooks, dataset licences, the user's answers.
- *Pitfalls:* invented budgets; listing risks that never come back in EV.2.

**BU.3 Determine data mining goals.** Outputs: data mining goals, data mining success criteria.
- *The report states:* the translation of the business objective into a technical task (classification, regression, detection, segmentation, forecasting, clustering, recommendation, …): inputs, outputs, and **technical success criteria** (metric, threshold, data split). For example: "mAP@0.5 ≥ 0.80 on the held-out test set".
- *Evidence:* configs, evaluation scripts, the user's answers about thresholds.
- *Pitfalls:* thresholds invented after seeing the results. If no threshold was fixed in advance, say so honestly and use a baseline comparison instead.

**BU.4 Produce project plan.** Outputs: project plan, initial assessment of tools and techniques.
- *The report states:* phases and milestones (a Gantt chart only when real dates exist; git history can supply them), and the initial choice of tools and techniques. Justify that choice in Chapter 2 and cross-reference it.
- *Pitfalls:* a perfectly linear Gantt chart that hides the real iterations; dates that don't match the history.

### Phase 2: Data understanding

**DU.1 Collect initial data.** Output: initial data collection report.
- *The report states:* every source (public dataset, company export, scraped, self-collected), how and when it was acquired, the licence or permission to use it, and problems met during collection.
- *Evidence:* download scripts, dataset cards, `data/README`, DVC files, notebook cells that load data.
- *Pitfalls:* no provenance; no licence; private data described too precisely.

**DU.2 Describe data.** Output: data description report.
- *The report states:* format, volume (rows, images, files, hours), schema or fields with types and units, classes and their counts, time span. A table is usually best.
- *Evidence:* compute it from the data with a script and record the command. Never copy numbers from memory.
- *Pitfalls:* numbers that disagree with the split sizes later; class counts that don't add up.

**DU.3 Explore data.** Output: data exploration report.
- *The report states:* distributions, class balance, correlations, representative samples (anonymized), and the observations that shaped later decisions (e.g. "night images are 4% of the set", which leads to augmentation in DP.3).
- *Evidence:* EDA notebooks and plots regenerated from the real data.
- *Pitfalls:* decorative plots with no conclusion drawn from them.

**DU.4 Verify data quality.** Output: data quality report.
- *The report states:* completeness (missing values), correctness (label noise, wrong units), duplicates, outliers, consistency across sources, and sampling bias, each **quantified** wherever possible.
- *Pitfalls:* "the data was of good quality" without a single number.

### Phase 3: Data preparation

**DP.1 Select data.** Output: rationale for inclusion and exclusion.
- *The report states:* which records, attributes and time ranges were kept or dropped, and why (relevance, quality, legal, compute).

**DP.2 Clean data.** Output: data cleaning report.
- *The report states:* for each quality issue from DU.4, the action taken and its effect (counts before and after), or the reason it was left alone.
- *Pitfalls:* cleaning steps with no link to a detected issue; issues from DU.4 that disappear silently.

**DP.3 Construct data.** Outputs: derived attributes, generated records.
- *The report states:* feature engineering (formulas), augmentation or synthetic samples (techniques and parameters), and the reasons for each.

**DP.4 Integrate data.** Output: merged data.
- *The report states:* how sources were joined or aggregated, the join keys, and conflicts resolved. With a single source this is usually **N/A**: use `\crispdm[na]{DP.4}` and one sentence saying so.

**DP.5 Format data.** Output: reformatted data (and the final dataset with its description).
- *The report states:* the syntactic changes the modelling tool requires (label format conversion, tokenization, resizing, normalization, encoding, file layout), and a short description of the final dataset handed to modelling.

### Phase 4: Modeling

**MO.1 Select modeling technique.** Outputs: modeling technique, modeling assumptions.
- *The report states:* candidate techniques, the chosen one(s) and why (linking to Chapter 2's comparison), and the assumptions they make (i.i.d. samples, class balance, stationarity, input size).

**MO.2 Generate test design.** Output: test design.
- *The report states:* how data was split (proportions, stratification, temporal or group split, leakage prevention), the validation protocol (hold-out or k-fold), the metrics, the baseline, and how the final test set was kept untouched. This is decided **before** assessment.
- *Pitfalls:* tuning on the test set; random splits on time-series or grouped data; no baseline.

**MO.3 Build model.** Outputs: parameter settings, models, model descriptions.
- *The report states:* the architecture, a hyperparameter table, the training procedure (epochs, optimizer, schedule, seeds), hardware and training time, and training curves drawn from real logs.

**MO.4 Assess model.** Outputs: model assessment, revised parameter settings.
- *The report states:* metrics with formulas and plain-language definitions; results per split (validation and held-out test kept separate); comparison of variants; the tuning iterations and what changed. This is the *technical* judgement against the BU.3 criteria.
- *Pitfalls:* a single number with no split, unit or variance; claims like "highly accurate" with no context.

### Phase 5: Evaluation

**EV.1 Evaluate results.** Outputs: assessment of results against the business success criteria, approved models.
- *The report states:* for **each** BU.1 criterion, whether the chosen model meets it, with evidence; which model is approved and why. This is a *business* judgement, which makes it different from MO.4. If no field test was possible, say what proxy was used and what still needs real-world validation.
- *Pitfalls:* simply repeating the MO.4 metrics (the most common failure in student reports).

**EV.2 Review process.** Output: review of the process.
- *The report states:* a quality check of the whole process: steps skipped or rushed, leakage checks, risks from BU.2 that materialized, threats to validity, error analysis with representative failures.

**EV.3 Determine next steps.** Outputs: list of possible actions, decision.
- *The report states:* the options (deploy, iterate, collect more data, stop) and the decision taken, with its reasons.

### Phase 6: Deployment

**DE.1 Plan deployment.** Output: deployment plan.
- *The report states:* how the model reaches its users (API, web or mobile app, edge device, batch job), separating what is **implemented** from what is **proposed**. Include an integration diagram if helpful.

**DE.2 Plan monitoring and maintenance.** Output: monitoring and maintenance plan.
- *The report states:* what is monitored (input drift, prediction quality, latency), retraining triggers, ownership. In student projects this is usually a *proposal*. Label it that way.

**DE.3 Produce final report.** Outputs: final report, final presentation.
- *The report states:* nothing extra. This document is the final report. Mention it in the General Introduction's "organization of the report" paragraph, where the marker sits.

**DE.4 Review project.** Output: experience documentation.
- *The report states:* lessons learned in the General Conclusion: what worked, what didn't, what you would do differently, with specifics.

---

## 3. Golden threads

A CRISP-DM report is coherent when the phases reference each other. Check each thread, and fix the side that breaks it:

1. **BU.1 → EV.1.** Every business success criterion is explicitly evaluated, as met, not met or not measurable yet.
2. **BU.3 → MO.4 → EV.1.** The technical criterion is measured on exactly the data split defined for it, then used to approve or reject a model.
3. **DU.4 → DP.2.** Every quality issue has a cleaning action or a justified decision to leave it.
4. **DU.3 → DP.3 / MO.1.** Exploration findings (imbalance, skew, rare conditions) explain preparation and modelling choices.
5. **DU.2 → DP.* → MO.2.** Counts add up: raw size − exclusions ± augmentation = train + validation + test.
6. **MO.2 → MO.4.** Reported numbers come from the declared test design; no tuning on the test set.
7. **BU.2 → EV.2.** Listed risks are revisited: did they happen, and was the mitigation used?
8. **EV.3 → DE.1 → General Conclusion.** The decision, the deployment plan and the future work tell the same story.
9. **Abstract ↔ Chapter 4.** Every number in the abstract appears identically in the results.

---

## 4. Presenting CRISP-DM honestly

**Iterations.** CRISP-DM is a cycle, not a waterfall: the arrows between phases go back and forth. In §3.2 (methodology), describe the loops that actually happened, such as "after the first model assessment, recall on class X was 0.41, so we returned to data preparation and added targeted augmentation". Support them with evidence (git history, notebook versions, experiment logs). Real loops make the methodology credible. Invented ones are dangerous at the defence.

**N/A tasks.** Not every task applies to every project. Mark them `\crispdm[na]{ID}` and explain why in one to three sentences. Typical honest N/As: DP.4 with a single data source; DE.2 when the project ends at a prototype (better still, write the monitoring plan as a proposal). The checker accepts an N/A only when the reason is written down.

**Deployment status.** Use precise words: *deployed* (running and used), *integrated* (wired into an application, demonstrated), *prototype* (runs locally), *planned* (designed, not built). Examiners check this.

---

## 5. Citing CRISP-DM and its alternatives

The template's `references.bib` contains verified entries:

| Key | Use it for |
| --- | --- |
| `chapman2000crisp` | The CRISP-DM 1.0 guide: phases, tasks, outputs. Cite it when introducing the methodology and in the cycle figure caption. |
| `wirth2000crisp` | The paper introducing CRISP-DM as a standard process model |
| `schroer2021crisp` | Systematic literature review of how CRISP-DM is applied (supports "widely used" claims) |
| `martinezplumed2021crisp` | CRISP-DM twenty years later: limits and extensions toward data-science trajectories (useful for justifying adaptations) |
| `fayyad1996kdd` | The KDD process, the main alternative to compare against |

When justifying the choice of CRISP-DM (Chapter 3, §3.2), compare it briefly with the KDD process and, if relevant, SEMMA or Microsoft TDSP. Cite only sources you have verified, and add any new ones to `references.bib` with full metadata. The `phd-skills:factcheck` skill, if installed, can verify BibTeX entries.

---

## 6. When CRISP-DM does not fit

CRISP-DM describes projects whose core is learning from data. If the project has no data analysis or modelling (a web or mobile app, a SaaS product, an embedded system), forcing the six phases produces empty, unconvincing sections. Tell the user, and use the process that was really followed (Scrum or another agile method, a V-model, design science research), with its own evidence (sprints, user stories, tests).

For **hybrid projects** (an application around an ML model), apply CRISP-DM to the data and model part and describe the software process for the rest. DE.1 then becomes the bridge: how the model is integrated into the application.
