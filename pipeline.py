"""
Data Processing Pipeline - CLI
DS 3500 - MP1
Usage:
python pipeline.py --input fixtures/sample.csv --config config.yaml --output cleaned_data.csv
python pipeline.py --input fixtures/sample.csv --config config.yaml --output cleaned_data.csv --verbose
"""
import argparse
import logging
import sys
from pathlib import Path

from data_loaders import load_data
from data_processor import process_data, create_cleaning_report

logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Load, clean and save a CSV file using a YAML config."
    )
    parser.add_argument(
        "-i", "--input", required=True,
        help="Path to the input file",
    )
    parser.add_argument(
        "-c", "--config", required=True,
        help="Path to the YAML configuration file",
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="Path for the cleaned CSV output",
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
        logger.error("Input file not found: %s", filepath)
        return False
    if not path.is_file():
        logger.error("Input path is not a file: %s", filepath)
        return False
    logger.info("Input file validated: %s", filepath)
    return True


def print_report(report):
    """Print the cleaning report, one key per line."""
    print("{")
    items = list(report.items())
    for i, (key, value) in enumerate(items):
        comma = "," if i < len(items) - 1 else ""
        print(f"    '{key}': {value}{comma}")
    print("}")


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(
        "Arguments parsed: input=%s, config=%s, output=%s",
        args.input, args.config, args.output,
    )

    # Validate both files before loading anything
    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    # Load data and configuration
    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    # Process
    df_before = data.copy()
    try:
        df_after = process_data(data, config)
    except ValueError:
        sys.exit(1)

    # Report and save
    report = create_cleaning_report(df_before, df_after)
    print_report(report)
    logger.info(
        "Processing complete: %d → %d rows",
        report["rows_before"], report["rows_after"],
    )

    df_after.to_csv(args.output, index=False)
    logger.info("Saved cleaned data to %s", args.output)


if __name__ == "__main__":
    main()
