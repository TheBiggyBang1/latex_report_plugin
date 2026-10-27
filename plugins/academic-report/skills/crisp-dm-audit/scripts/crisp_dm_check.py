#!/usr/bin/env python3
r"""Check that a LaTeX report addresses every CRISP-DM generic task.

Tasks are marked in the LaTeX sources with \crispdm{ID} right under the heading
of the section that addresses them, or \crispdm[na]{ID} when the task does not
apply and the section explains why. Starting from main.tex and following
\input/\include, the script finds every marker, measures the prose of the
enclosing section (including its subsections), and reports each of the 24
CRISP-DM 1.0 generic tasks as:

  OK          addressed with enough prose
  N/A         declared not applicable, with a written justification
  UNVERIFIED  addressed, but the section still contains [TO VERIFY] markers
  THIN        marker present but too little prose (or an N/A without reasons)
  MISSING     no marker anywhere

Usage:
  python crisp_dm_check.py [REPORT_DIR] [--main main.tex] [--min-words 80]
                           [--na-min-words 15] [--strict] [--json]

Exit status: 0 when every task is OK or N/A (UNVERIFIED also passes unless
--strict), 1 when gaps remain, 2 when the report cannot be read.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

PHASES = {
    "BU": "Business understanding",
    "DU": "Data understanding",
    "DP": "Data preparation",
    "MO": "Modeling",
    "EV": "Evaluation",
    "DE": "Deployment",
}

TASKS = {
    "BU.1": "Determine business objectives",
    "BU.2": "Assess situation",
    "BU.3": "Determine data mining goals",
    "BU.4": "Produce project plan",
    "DU.1": "Collect initial data",
    "DU.2": "Describe data",
    "DU.3": "Explore data",
    "DU.4": "Verify data quality",
    "DP.1": "Select data",
    "DP.2": "Clean data",
    "DP.3": "Construct data",
    "DP.4": "Integrate data",
    "DP.5": "Format data",
    "MO.1": "Select modeling technique",
    "MO.2": "Generate test design",
    "MO.3": "Build model",
    "MO.4": "Assess model",
    "EV.1": "Evaluate results",
    "EV.2": "Review process",
    "EV.3": "Determine next steps",
    "DE.1": "Plan deployment",
    "DE.2": "Plan monitoring and maintenance",
    "DE.3": "Produce final report",
    "DE.4": "Review project",
}

PASSING = {"OK", "N/A"}

HEADING_LEVELS = {"part": -1, "chapter": 0, "section": 1, "subsection": 2,
                  "subsubsection": 3, "paragraph": 4}
HEADING_RE = re.compile(
    r"\\(part|chapter|section|subsection|subsubsection|paragraph)\*?\s*"
    r"(?:\[[^\]]*\])?\s*\{((?:[^{}]|\{[^{}]*\})*)\}")
MARKER_RE = re.compile(r"\\crispdm\s*(?:\[([^\]]*)\])?\s*\{([^{}]*)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\s*\{([^{}]+)\}")
VERIFY_RE = re.compile(r"\\toverify\s*\{|\[\s*TO VERIFY", re.IGNORECASE)
DEFINITION_RE = re.compile(
    r"\\(?:newcommand|renewcommand|providecommand|DeclareRobustCommand|"
    r"NewDocumentCommand)\*?\s*\{?\s*\\crispdm\b|\\def\s*\\crispdm\b")
MATRIX_RE = re.compile(r"\\crisploc\s*\{|\\(?:ref|pageref|hyperref)\s*[\[{]crisp:")
COMMENT_RE = re.compile(r"(?<!\\)%.*")
# Commands whose braced arguments are keys, paths, labels or running heads
# rather than prose.
NON_PROSE_RE = re.compile(
    r"\\(?:addcontentsline|markboth)(?:\s*\{[^{}]*\})+|"
    r"\\(?:label|ref|eqref|pageref|autoref|nameref|[cC]ref|cite\w*|crispdm|"
    r"crisploc|input|include|includegraphics|url|addbibresource|begin|end|"
    r"hyperref|graphicspath)\*?(?:\s*\[[^\]]*\])*\s*\{[^{}]*\}")
COMMAND_RE = re.compile(r"\\[A-Za-z@]+\*?")
WORD_RE = re.compile(r"[^\W_]+(?:['\u2019-][^\W_]+)*")


@dataclass
class Location:
    file: str
    line: int
    heading: str
    words: int
    not_applicable: bool
    unverified: bool


@dataclass
class TaskResult:
    task_id: str
    phase: str
    name: str
    status: str = "MISSING"
    words: int = 0
    locations: list[Location] = field(default_factory=list)


def strip_comments(text: str) -> str:
    """Remove LaTeX comments while keeping line numbers intact."""
    return "\n".join(COMMENT_RE.sub("", line) for line in text.split("\n"))


def display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def read_tex(path: Path) -> str:
    return strip_comments(path.read_text(encoding="utf-8", errors="replace"))


def resolve_sources(report_dir: Path, main: str) -> tuple[list[Path], list[str]]:
    """Return main.tex and every file it pulls in, in document order.

    LaTeX resolves \\input paths against the directory of main.tex, not the
    including file, so every path is joined to report_dir.
    """
    found: list[Path] = []
    missing: list[str] = []
    seen: set[Path] = set()

    def visit(path: Path) -> None:
        path = path.resolve()
        if path in seen:
            return
        seen.add(path)
        if not path.is_file():
            missing.append(display_path(path, report_dir))
            return
        found.append(path)
        for match in INPUT_RE.finditer(read_tex(path)):
            child = report_dir / match.group(1).strip()
            if child.suffix != ".tex":
                child = child.with_name(child.name + ".tex")
            visit(child)

    visit(report_dir / main)
    return found, missing


def count_words(latex: str) -> int:
    text = NON_PROSE_RE.sub(" ", latex)
    text = COMMAND_RE.sub(" ", text)
    return len(WORD_RE.findall(text))


def clean_heading(title: str) -> str:
    title = COMMAND_RE.sub("", title).replace("{", "").replace("}", "").replace("~", " ")
    title = " ".join(title.split())
    return title if len(title) <= 48 else title[:45] + "..."


def scan_file(path: Path, report_dir: Path, results: dict[str, TaskResult],
              seen: set[tuple[str, str, int]], warnings: list[str]) -> None:
    """Attach every \\crispdm marker in one file to its task.

    `seen` holds (task, file, section start) so that two markers for the same
    task inside one section do not count its words twice.
    """
    text = read_tex(path)
    name = display_path(path, report_dir)
    headings = [(m.start(), m.end(), HEADING_LEVELS[m.group(1)], clean_heading(m.group(2)))
                for m in HEADING_RE.finditer(text)]

    for marker in MARKER_RE.finditer(text):
        task_id = marker.group(2).strip()
        line = text.count("\n", 0, marker.start()) + 1
        if task_id not in TASKS:
            warnings.append(f"{name}:{line}: unknown CRISP-DM task ID '{task_id}'")
            continue

        # The enclosing section runs from its heading to the next heading of the
        # same or a higher level, so its subsections count towards it.
        start, level, heading = 0, -2, f"(top of {name})"
        for h_start, h_end, h_level, h_title in headings:
            if h_start < marker.start():
                start, level, heading = h_end, h_level, h_title
        end = next((h_start for h_start, _, h_level, _ in headings
                    if h_start > start and h_level <= level), len(text))

        region = text[start:end]
        key = (task_id, name, start)
        results[task_id].locations.append(Location(
            file=name,
            line=line,
            heading=heading,
            words=0 if key in seen else count_words(region),
            not_applicable=(marker.group(1) or "").strip().lower() in {"na", "n/a"},
            unverified=bool(VERIFY_RE.search(region)),
        ))
        seen.add(key)


def classify(result: TaskResult, min_words: int, na_min_words: int) -> str:
    if not result.locations:
        return "MISSING"
    result.words = sum(loc.words for loc in result.locations)
    not_applicable = all(loc.not_applicable for loc in result.locations)
    if result.words < (na_min_words if not_applicable else min_words):
        return "THIN"
    if any(loc.unverified for loc in result.locations):
        return "UNVERIFIED"
    return "N/A" if not_applicable else "OK"


def check(report_dir: Path, main: str, min_words: int, na_min_words: int) -> dict:
    sources, missing_files = resolve_sources(report_dir, main)
    if not sources:
        raise FileNotFoundError(f"{report_dir / main} not found")

    warnings = [f"included file not found: {name}" for name in missing_files]
    results = {task_id: TaskResult(task_id, PHASES[task_id[:2]], name)
               for task_id, name in TASKS.items()}
    seen: set[tuple[str, str, int]] = set()
    full_text = ""
    for path in sources:
        scan_file(path, report_dir, results, seen, warnings)
        full_text += read_tex(path)

    for result in results.values():
        result.status = classify(result, min_words, na_min_words)

    if not DEFINITION_RE.search(full_text):
        warnings.append("\\crispdm is never defined: add the macros from the template preamble")
    if not MATRIX_RE.search(full_text):
        warnings.append("no CRISP-DM traceability table found (\\crisploc / \\ref{crisp:...})")

    phases = {}
    for prefix, phase in PHASES.items():
        tasks = [r for r in results.values() if r.task_id.startswith(prefix)]
        phases[phase] = {"complete": sum(r.status in PASSING for r in tasks),
                         "total": len(tasks)}

    return {
        "report_dir": str(report_dir),
        "files": [display_path(p, report_dir) for p in sources],
        "tasks": [asdict(r) for r in results.values()],
        "phases": phases,
        "warnings": warnings,
    }


def passed(report: dict, strict: bool) -> bool:
    allowed = PASSING if strict else PASSING | {"UNVERIFIED"}
    return all(task["status"] in allowed for task in report["tasks"])


def print_text(report: dict, strict: bool) -> None:
    print(f"CRISP-DM coverage check: {report['report_dir']} ({len(report['files'])} files)\n")
    print(f"  {'ID':<5} {'Generic task':<33} {'Status':<11} {'Words':>5}  Where")
    current_phase = None
    for task in report["tasks"]:
        if task["phase"] != current_phase:
            current_phase = task["phase"]
            phase = report["phases"][current_phase]
            print(f"{current_phase} ({phase['complete']}/{phase['total']} complete)")
        where = "-"
        if task["locations"]:
            first = task["locations"][0]
            where = f"{first['file']}:{first['line']}  {first['heading']}"
            if len(task["locations"]) > 1:
                where += f"  (+{len(task['locations']) - 1} more)"
        print(f"  {task['task_id']:<5} {task['name']:<33} {task['status']:<11} "
              f"{task['words']:>5}  {where}")

    counts = {}
    for task in report["tasks"]:
        counts[task["status"]] = counts.get(task["status"], 0) + 1
    order = ["OK", "N/A", "UNVERIFIED", "THIN", "MISSING"]
    summary = ", ".join(f"{counts.get(s, 0)} {s}" for s in order)
    complete = sum(p["complete"] == p["total"] for p in report["phases"].values())
    print(f"\nResult: {summary} -> {complete}/{len(report['phases'])} phases complete")
    print("PASS" if passed(report, strict) else "FAIL")
    if not strict and counts.get("UNVERIFIED"):
        print("Note: UNVERIFIED tasks pass without --strict; run with --strict before submission.")
    if report["warnings"]:
        print("\nWarnings:")
        for warning in report["warnings"]:
            print(f"  - {warning}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("report_dir", nargs="?", default="report",
                        help="directory containing main.tex (default: report)")
    parser.add_argument("--main", default="main.tex", help="root LaTeX file")
    parser.add_argument("--min-words", type=int, default=80,
                        help="minimum prose words for an addressed task (default: 80)")
    parser.add_argument("--na-min-words", type=int, default=15,
                        help="minimum words justifying an N/A task (default: 15)")
    parser.add_argument("--strict", action="store_true",
                        help="also fail on UNVERIFIED tasks (use before submission)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a table")
    args = parser.parse_args()

    sys.stdout.reconfigure(errors="replace")
    try:
        report = check(Path(args.report_dir).resolve(), args.main,
                       args.min_words, args.na_min_words)
    except (FileNotFoundError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    report["passed"] = passed(report, args.strict)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_text(report, args.strict)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
