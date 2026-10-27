#!/usr/bin/env python3
"""Compile a LaTeX report and summarize what still needs fixing.

Runs ENGINE -> biber (or bibtex) -> ENGINE -> ENGINE, plus extra passes while
LaTeX asks for a rerun, then copies main.pdf to REPORT.pdf and lists undefined
references and citations, duplicate labels and overfull boxes from the log.
It needs neither Perl nor latexmk, so it works with a plain MiKTeX install.

Usage:
  python build_report.py [REPORT_DIR] [--main main.tex]
                         [--engine pdflatex|lualatex|xelatex] [--strict]

Exit status: 0 on a clean build, 1 on errors (or on warnings with --strict),
2 when a required program is missing.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

INSTALL_HINT = ("Install MiKTeX (https://miktex.org/download) or TeX Live "
                "(https://tug.org/texlive/), then open a new terminal; or zip the "
                "report folder and compile it in Overleaf.")
MAX_PASSES = 5
PASS_TIMEOUT = 600  # seconds; a first MiKTeX run may download packages

RERUN_RE = re.compile(r"Rerun to get|Please rerun LaTeX|Label\(s\) may have changed|"
                      r"Please \(re\)run Biber")
ERROR_RE = re.compile(r"^(?:\S+\.tex:\d+: .*|! .*)$", re.MULTILINE)
WARNINGS = {
    "undefined references": re.compile(r"Reference [`']([^']+)' on page \S+ undefined"),
    "undefined citations": re.compile(r"Citation [`']([^']+)' on page \S+ undefined"),
    "multiply defined labels": re.compile(r"Label [`']([^']+)' multiply defined"),
}
OVERFULL_RE = re.compile(r"Overfull \\hbox \(([\d.]+)pt too wide\) .*?lines? ([\d-]+)")


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                          errors="replace", timeout=PASS_TIMEOUT)


def read_log(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def latex_pass(engine: str, main: str, report_dir: Path, number: int) -> str:
    """Run one LaTeX pass and return its log; exit on a fatal error."""
    print(f"[{number}] {engine} {main}")
    result = run([engine, "-interaction=nonstopmode", "-halt-on-error",
                  "-file-line-error", main], report_dir)
    log = read_log(report_dir / Path(main).with_suffix(".log"))
    if result.returncode != 0:
        errors = ERROR_RE.findall(log) or result.stdout.splitlines()[-15:]
        print(f"\nLaTeX failed (exit {result.returncode}). First errors:")
        for line in errors[:10]:
            print(f"  {line}")
        sys.exit(1)
    return log


def bibliography_tool(main_source: str) -> str | None:
    if "\\addbibresource" in main_source:
        return "biber"
    if re.search(r"\\bibliography\s*\{", main_source):
        return "bibtex"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("report_dir", nargs="?", default="report",
                        help="directory containing main.tex (default: report)")
    parser.add_argument("--main", default="main.tex", help="root LaTeX file")
    parser.add_argument("--engine", default="pdflatex",
                        choices=["pdflatex", "lualatex", "xelatex"])
    parser.add_argument("--strict", action="store_true",
                        help="fail on undefined references/citations and overfull boxes")
    args = parser.parse_args()

    sys.stdout.reconfigure(errors="replace")
    report_dir = Path(args.report_dir).resolve()
    main_tex = report_dir / args.main
    if not main_tex.is_file():
        print(f"error: {main_tex} not found", file=sys.stderr)
        return 2
    if not shutil.which(args.engine):
        print(f"error: {args.engine} not found. {INSTALL_HINT}", file=sys.stderr)
        return 2
    bib_tool = bibliography_tool(main_tex.read_text(encoding="utf-8", errors="replace"))
    if bib_tool and not shutil.which(bib_tool):
        print(f"error: {bib_tool} not found (it ships with MiKTeX and TeX Live). "
              f"{INSTALL_HINT}", file=sys.stderr)
        return 2

    stem = main_tex.stem
    try:
        log = latex_pass(args.engine, args.main, report_dir, 1)
        if bib_tool:
            print(f"[-] {bib_tool} {stem}")
            result = run([bib_tool, stem], report_dir)
            bib_log = read_log(report_dir / f"{stem}.blg")
            problems = [line for line in bib_log.splitlines()
                        if re.search(r"\b(ERROR|WARN)\b|^Warning--|error message", line)]
            if result.returncode != 0 or problems:
                print(f"{bib_tool} reported:")
                for line in problems[:15] or result.stdout.splitlines()[-15:]:
                    print(f"  {line}")
                if result.returncode != 0:
                    return 1
        passes = 1
        while passes < 3 or (RERUN_RE.search(log) and passes < MAX_PASSES):
            passes += 1
            log = latex_pass(args.engine, args.main, report_dir, passes)
    except subprocess.TimeoutExpired as error:
        print(f"error: '{' '.join(error.cmd)}' took longer than {PASS_TIMEOUT}s. "
              "If MiKTeX is waiting for a package-install dialog, enable automatic "
              "package installation in MiKTeX Console.", file=sys.stderr)
        return 1

    pdf = report_dir / f"{stem}.pdf"
    final = report_dir / "REPORT.pdf"
    try:
        shutil.copyfile(pdf, final)
    except PermissionError:
        print(f"error: cannot overwrite {final}; close it in your PDF viewer and rerun.",
              file=sys.stderr)
        return 1

    found_any = False
    print(f"\nBuilt {final} ({passes} LaTeX passes)")
    for label, pattern in WARNINGS.items():
        keys = sorted(set(pattern.findall(log)))
        if keys:
            found_any = True
            print(f"  {len(keys)} {label}: {', '.join(keys[:10])}")
    overfull = [(float(width), lines) for width, lines in OVERFULL_RE.findall(log)
                if float(width) > 1.0]
    if overfull:
        found_any = True
        print(f"  {len(overfull)} overfull boxes > 1pt (widest first; lines refer to "
              f"the file being read at that point of the log):")
        for width, lines in sorted(overfull, reverse=True)[:5]:
            print(f"    {width:.1f}pt too wide at lines {lines}")
    if not found_any:
        print("  No undefined references, citations, duplicate labels or overfull boxes.")
    return 1 if args.strict and found_any else 0


if __name__ == "__main__":
    sys.exit(main())
