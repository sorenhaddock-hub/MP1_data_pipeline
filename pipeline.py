"""
Data Processing Pipeline - CLI Template
DS 3500 - MP1
Usage:
python pipeline.py --input data.csv --output clean.csv
python pipeline.py --input data.csv --output results.json --format json --verbose
"""
import argparse
import csv
import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stderr,
    )
    logger.debug("Verbose logging enabled")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Clean a CSV file and write it out as CSV or JSON."
    )
    parser.add_argument(
        "-i", "--input", required=True, type=Path,
        help="Path to the input CSV file",
    )
    parser.add_argument(
        "-o", "--output", required=True, type=Path,
        help="Path for the output file",
    )
    parser.add_argument(
        "-f", "--format", choices=["csv", "json"], default="csv",
        help="Output format (default: csv)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Enable debug-level logging",
    )
    return parser.parse_args()


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    path = Path(filepath)
    if not path.exists():
        logger.error("Input path does not exist: %s", path)
        return False
    if not path.is_file():
        logger.error("Input path is not a file: %s", path)
        return False
    logger.debug("Input file validated: %s", path)
    return True


def load_data(filepath):
    """Read a CSV file into a list of dicts."""
    with open(filepath, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    logger.info("Loaded %d rows from %s", len(rows), filepath)
    return rows


def clean_data(rows):
    """Strip whitespace from values and drop fully empty rows."""
    cleaned = []
    for row in rows:
        stripped = {
            (k.strip() if k else k): (v.strip() if isinstance(v, str) else v)
            for k, v in row.items()
        }
        if any(v for v in stripped.values()):
            cleaned.append(stripped)
    logger.info("Dropped %d empty rows", len(rows) - len(cleaned))
    return cleaned


def write_output(rows, filepath, fmt):
    """Write rows to CSV or JSON."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    if fmt == "json":
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2)
    else:
        fieldnames = list(rows[0].keys()) if rows else []
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    logger.info("Wrote %d rows to %s (%s)", len(rows), filepath, fmt)


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug("Arguments: %s", vars(args))

    if not validate_input(args.input):
        sys.exit(1)

    try:
        rows = load_data(args.input)
        rows = clean_data(rows)
        write_output(rows, args.output, args.format)
    except (OSError, csv.Error) as e:
        logger.error("Pipeline failed: %s", e)
        sys.exit(1)

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()