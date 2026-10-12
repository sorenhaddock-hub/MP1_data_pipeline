"""
Data Processing Pipeline - CLI
DS 3500 - MP1
Usage:
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
"""
import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Load, validate, clean and save a CSV file using a YAML config."
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


def print_report(report):
    """Print the cleaning report, one key per line."""
    print("\nCleaning report:")
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

    # Validate the data
    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]
    rows_loaded = len(data)
    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info("Validation complete: %d -> %d rows", rows_loaded, len(data))

    # Process
    df_before = data.copy()
    try:
        df_after = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(df_before, df_after)
    logger.info(
        "Processing complete: %d -> %d rows",
        report["rows_before"], report["rows_after"],
    )

    # Save
    output_path = save_data(df_after, args.output)
    logger.info("Saved cleaned data to %s", output_path)

    print_report(report)


if __name__ == "__main__":
    main()
