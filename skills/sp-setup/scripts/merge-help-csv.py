#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""Merge module help entries into shared bmad-help.csv.

Reads a source CSV with module help entries and merges them into a target CSV.
Uses an anti-zombie pattern: all existing rows matching the source module code
are removed before appending fresh rows.

Supports two target CSV formats:
- V2 (13 columns): the format documented by bmad-help SKILL.md
- V1 (16 columns): legacy format from older BMB installers

When the target uses the V1 format, all existing rows are automatically
converted to V2 before merging. The output is always V2 format.

Legacy cleanup: when --legacy-dir and --module-code are provided, deletes old
per-module module-help.csv files from {legacy-dir}/{module-code}/ and
{legacy-dir}/core/. Only the current module and core are touched.

Exit codes: 0=success, 1=validation error, 2=runtime error
"""

import argparse
import csv
import json
import sys
from io import StringIO
from pathlib import Path

# V2 header (13 columns) — the format bmad-help SKILL.md documents
V2_HEADER = [
    "module",
    "skill",
    "display-name",
    "menu-code",
    "description",
    "action",
    "args",
    "phase",
    "after",
    "before",
    "required",
    "output-location",
    "outputs",
]

# V1 header (16 columns) — legacy format from older BMB installers
V1_HEADER = [
    "module",
    "phase",
    "name",
    "code",
    "sequence",
    "workflow-file",
    "command",
    "required",
    "agent-name",
    "agent-command",
    "agent-display-name",
    "agent-title",
    "options",
    "description",
    "output-location",
    "outputs",
]

# Column mapping: V1 field name → V2 field index
_V1_TO_V2_MAP = {
    "module": 0,
    "name": 2,           # → display-name
    "code": 3,           # → menu-code
    "workflow-file": 1,  # → skill
    "command": 5,        # → action
    "options": 6,        # → args
    "phase": 7,
    "required": 10,
    "description": 4,
    "output-location": 11,
    "outputs": 12,
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge module help entries into shared bmad-help.csv with anti-zombie pattern."
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Path to the target bmad-help.csv file",
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path to the source module-help.csv with entries to merge",
    )
    parser.add_argument(
        "--legacy-dir",
        help="Path to _bmad/ directory to check for legacy per-module CSV files.",
    )
    parser.add_argument(
        "--module-code",
        help="Module code (required with --legacy-dir for scoping cleanup).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed progress to stderr",
    )
    return parser.parse_args()


def read_csv_rows(path: str) -> tuple[list[str], list[list[str]]]:
    """Read CSV file returning (header, data_rows).

    Returns empty header and rows if file doesn't exist.
    """
    file_path = Path(path)
    if not file_path.exists():
        return [], []

    with open(file_path, "r", encoding="utf-8", newline="") as f:
        content = f.read()

    reader = csv.reader(StringIO(content))
    rows = list(reader)

    if not rows:
        return [], []

    return rows[0], rows[1:]


def detect_format(header: list[str]) -> str:
    """Detect whether a CSV header is V1 (16-col) or V2 (13-col).

    Returns "v1", "v2", or "unknown".
    """
    header_set = set(h.strip() for h in header)
    if header_set == set(V1_HEADER):
        return "v1"
    if header_set == set(V2_HEADER):
        return "v2"
    # Check for partial matches
    if "workflow-file" in header_set and "agent-name" in header_set:
        return "v1"
    if "skill" in header_set and "after" in header_set:
        return "v2"
    return "unknown"


def convert_v1_to_v2_rows(rows: list[list[str]], verbose: bool = False) -> list[list[str]]:
    """Convert V1 (16-column) rows to V2 (13-column) format.

    Mapping:
      V1 module      → V2 module
      V1 workflow-file → V2 skill
      V1 name        → V2 display-name
      V1 code        → V2 menu-code
      V1 description → V2 description
      V1 command     → V2 action
      V1 options     → V2 args
      V1 phase       → V2 phase
      (new)          → V2 after (empty)
      (new)          → V2 before (empty)
      V1 required    → V2 required
      V1 output-location → V2 output-location
      V1 outputs     → V2 outputs

    Dropped V1 fields: sequence, agent-name, agent-command,
                       agent-display-name, agent-title
    """
    # Build index map from V1 header
    v1_idx = {name: i for i, name in enumerate(V1_HEADER)}
    converted = []

    for row in rows:
        # Pad row to V1 column count if needed
        padded = list(row) + [""] * (len(V1_HEADER) - len(row))

        def get_v1(field: str) -> str:
            idx = v1_idx.get(field, -1)
            return padded[idx].strip() if 0 <= idx < len(padded) else ""

        v2_row = [
            get_v1("module"),          # 0: module
            get_v1("workflow-file"),    # 1: skill
            get_v1("name"),            # 2: display-name
            get_v1("code"),            # 3: menu-code
            get_v1("description"),     # 4: description
            get_v1("command"),         # 5: action
            get_v1("options"),         # 6: args
            get_v1("phase"),           # 7: phase
            "",                        # 8: after (not in V1)
            "",                        # 9: before (not in V1)
            get_v1("required"),        # 10: required
            get_v1("output-location"), # 11: output-location
            get_v1("outputs"),         # 12: outputs
        ]
        converted.append(v2_row)

    if verbose and converted:
        print(f"Converted {len(converted)} rows from V1 to V2 format", file=sys.stderr)

    return converted


def extract_module_codes(rows: list[list[str]]) -> set[str]:
    """Extract unique module codes from data rows."""
    codes = set()
    for row in rows:
        if row and row[0].strip():
            codes.add(row[0].strip())
    return codes


def filter_rows(rows: list[list[str]], module_code: str) -> list[list[str]]:
    """Remove all rows matching the given module code."""
    return [row for row in rows if not row or row[0].strip() != module_code]


def write_csv(path: str, header: list[str], rows: list[list[str]], verbose: bool = False) -> None:
    """Write header + rows to CSV file, creating parent dirs as needed."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"Writing {len(rows)} data rows to {path}", file=sys.stderr)

    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def cleanup_legacy_csvs(
    legacy_dir: str, module_code: str, verbose: bool = False
) -> list:
    """Delete legacy per-module module-help.csv files for this module and core only.

    Returns list of deleted file paths.
    """
    deleted = []
    for subdir in (module_code, "core"):
        legacy_path = Path(legacy_dir) / subdir / "module-help.csv"
        if legacy_path.exists():
            if verbose:
                print(f"Deleting legacy CSV: {legacy_path}", file=sys.stderr)
            legacy_path.unlink()
            deleted.append(str(legacy_path))
    return deleted


def main():
    args = parse_args()

    # Read source entries
    source_header, source_rows = read_csv_rows(args.source)
    if not source_rows:
        print(f"Error: No data rows found in source {args.source}", file=sys.stderr)
        sys.exit(1)

    # Validate source is V2 format
    source_format = detect_format(source_header) if source_header else "v2"
    if source_format not in ("v2", "unknown"):
        print(
            f"Error: Source CSV has unexpected format (expected V2/13-column, got {source_format})",
            file=sys.stderr,
        )
        sys.exit(1)

    # Normalize source rows to V2 (pad to 13 columns if needed)
    normalized_source = []
    for row in source_rows:
        padded = list(row) + [""] * (len(V2_HEADER) - len(row))
        normalized_source.append(padded[: len(V2_HEADER)])

    # Determine module codes being merged
    source_codes = extract_module_codes(normalized_source)
    if not source_codes:
        print("Error: Could not determine module code from source rows", file=sys.stderr)
        sys.exit(1)

    if args.verbose:
        print(f"Source module codes: {source_codes}", file=sys.stderr)
        print(f"Source rows: {len(normalized_source)}", file=sys.stderr)

    # Read existing target (may not exist)
    target_header, target_rows = read_csv_rows(args.target)
    target_existed = Path(args.target).exists()
    format_converted = False

    if args.verbose:
        print(f"Target exists: {target_existed}", file=sys.stderr)
        if target_existed:
            print(f"Existing target rows: {len(target_rows)}", file=sys.stderr)

    # Detect and convert target format if needed
    if target_header:
        target_format = detect_format(target_header)
        if args.verbose:
            print(f"Target format: {target_format}", file=sys.stderr)

        if target_format == "v1":
            # Convert V1 rows to V2
            target_rows = convert_v1_to_v2_rows(target_rows, args.verbose)
            format_converted = True
            if args.verbose:
                print("Converted target from V1 (16-col) to V2 (13-col) format", file=sys.stderr)
        elif target_format == "unknown":
            # Unknown format — convert if column count matches V1
            if len(target_header) == 16:
                target_rows = convert_v1_to_v2_rows(target_rows, args.verbose)
                format_converted = True
                if args.verbose:
                    print(
                        "Target has 16 columns (unknown header) — converting to V2 format",
                        file=sys.stderr,
                    )
            # Otherwise assume V2-compatible and proceed

    # Always write V2 format
    header = V2_HEADER

    # Anti-zombie: remove all rows for each source module code
    filtered_rows = target_rows
    removed_count = 0
    for code in source_codes:
        before_count = len(filtered_rows)
        filtered_rows = filter_rows(filtered_rows, code)
        removed_count += before_count - len(filtered_rows)

    if args.verbose and removed_count > 0:
        print(f"Removed {removed_count} existing rows (anti-zombie)", file=sys.stderr)

    # Append source rows
    merged_rows = filtered_rows + normalized_source

    # Write result
    write_csv(args.target, header, merged_rows, args.verbose)

    # Legacy cleanup: delete old per-module CSV files
    legacy_deleted = []
    if args.legacy_dir:
        if not args.module_code:
            print(
                "Error: --module-code is required when --legacy-dir is provided",
                file=sys.stderr,
            )
            sys.exit(1)
        legacy_deleted = cleanup_legacy_csvs(
            args.legacy_dir, args.module_code, args.verbose
        )

    # Output result summary as JSON
    result = {
        "status": "success",
        "target_path": str(Path(args.target).resolve()),
        "target_existed": target_existed,
        "format_converted": format_converted,
        "module_codes": sorted(source_codes),
        "rows_removed": removed_count,
        "rows_added": len(normalized_source),
        "total_rows": len(merged_rows),
        "legacy_csvs_deleted": legacy_deleted,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
