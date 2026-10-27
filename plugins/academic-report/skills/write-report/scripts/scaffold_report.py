#!/usr/bin/env python3
"""Copy the LaTeX report template into a project without overwriting anything.

Usage:
  python scaffold_report.py PROJECT_DIR [--dest report]

Existing files are left untouched and listed as skipped, so running the script
again only restores template files that were deleted.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "report-template"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("project_dir", help="root of the project the report is about")
    parser.add_argument("--dest", default="report",
                        help="report folder inside the project (default: report)")
    args = parser.parse_args()

    project = Path(args.project_dir).resolve()
    if not project.is_dir():
        print(f"error: {project} is not a directory", file=sys.stderr)
        return 2
    target = project / args.dest

    created, skipped = [], []
    for source in sorted(TEMPLATE.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(TEMPLATE)
        destination = target / relative
        if destination.exists():
            skipped.append(relative.as_posix())
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        created.append(relative.as_posix())

    print(f"Report folder: {target}")
    print(f"Created {len(created)} file(s)" + (":" if created else "."))
    for name in created:
        print(f"  + {name}")
    if skipped:
        print(f"Kept {len(skipped)} existing file(s) unchanged:")
        for name in skipped:
            print(f"  = {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
