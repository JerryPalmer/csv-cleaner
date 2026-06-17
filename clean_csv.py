#!/usr/bin/env python3
"""Remove rows that are entirely empty from a CSV.

Usage:
  python clean_csv.py input.csv output.csv [--encoding utf-8] [--sep ,] [--open-output]
"""
import argparse
import sys
import os
import logging
from pathlib import Path

import pandas as pd


LOG = logging.getLogger("csv_cleaner")


def setup_logging(level=logging.INFO):
    handler = logging.StreamHandler()
    fmt = "%(levelname)s: %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    LOG.addHandler(handler)
    LOG.setLevel(level)


def validate_paths(input_path: Path, output_path: Path) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    if not input_path.is_file():
        raise IsADirectoryError(f"Input path is not a file: {input_path}")

    outdir = output_path.parent
    if not outdir.exists():
        LOG.debug("Output directory does not exist; attempting to create: %s", outdir)
        try:
            outdir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise PermissionError(f"Cannot create output directory {outdir}: {e}")
    # Test write permission by attempting to open for append then close
    try:
        with open(output_path, "a", encoding="utf-8"):
            pass
    except Exception as e:
        raise PermissionError(f"Cannot write to output file {output_path}: {e}")


def open_output_file(path: str):
    try:
        if os.name == "nt":
            os.startfile(path)
        else:
            import subprocess
            import platform
            if platform.system() == "Darwin":
                subprocess.run(["open", path], check=False)
            else:
                subprocess.run(["xdg-open", path], check=False)
    except Exception as e:
        LOG.warning("Could not open file automatically: %s", e)


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    setup_logging()

    p = argparse.ArgumentParser(description="Remove empty rows from a CSV")
    p.add_argument("input_csv", help="Input CSV path")
    p.add_argument("output_csv", help="Output CSV path")
    p.add_argument("--encoding", default="utf-8", help="File encoding (default: utf-8)")
    p.add_argument("--sep", default=",", help="CSV delimiter (default: ,)")
    p.add_argument("--open-output", action="store_true", help="Open output file after writing (platform-specific)")
    p.add_argument("--quiet", action="store_true", help="Suppress informational output")
    args = p.parse_args(argv)

    input_path = Path(args.input_csv)
    output_path = Path(args.output_csv)

    try:
        validate_paths(input_path, output_path)
    except FileNotFoundError as e:
        LOG.error(e)
        sys.exit(2)
    except IsADirectoryError as e:
        LOG.error(e)
        sys.exit(3)
    except PermissionError as e:
        LOG.error(e)
        sys.exit(4)
    except Exception as e:
        LOG.error("Path validation failed: %s", e)
        sys.exit(5)

    try:
        # Read everything as strings so we can detect whitespace-only cells
        LOG.info("Reading CSV: %s", input_path)
        df = pd.read_csv(str(input_path), dtype=str, encoding=args.encoding, sep=args.sep, keep_default_na=False)
        rows_before = len(df)

        # Convert whitespace-only strings to NA and drop rows that are all NA
        df = df.replace(r"^\s*$", pd.NA, regex=True)
        df = df.dropna(how="all")
        rows_after = len(df)

        # Write output
        df.to_csv(str(output_path), index=False, encoding=args.encoding, sep=args.sep)

        if not args.quiet:
            LOG.info("Read %d rows; wrote %d rows; removed %d empty rows.", rows_before, rows_after, (rows_before - rows_after))

        if args.open_output:
            open_output_file(str(output_path))

    except pd.errors.EmptyDataError:
        LOG.error("Input CSV is empty: %s", input_path)
        sys.exit(6)
    except UnicodeDecodeError as e:
        LOG.error("Encoding error reading %s: %s", input_path, e)
        sys.exit(7)
    except pd.errors.ParserError as e:
        LOG.error("Error parsing CSV %s: %s", input_path, e)
        sys.exit(8)
    except Exception as e:
        LOG.exception("Unexpected error: %s", e)
        sys.exit(10)


if __name__ == "__main__":
    main()
