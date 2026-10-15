# MP1 Data Pipeline

This project is a command-line data pipeline that loads a CSV file, validates it, cleans it, and saves the result, with every cleaning decision controlled by a YAML configuration file instead of hard-coded values. Data moves through the pipeline in four stages: load, validate, process, and save. `pipeline.py` is the entry point; it parses the command-line arguments, checks that the input and config files exist, and coordinates the other modules. The reusable code lives in the `src/` package. `data_loaders.py` reads CSV, JSON, and YAML files based on their extension, and `data_validator.py` checks that the required columns exist and removes rows whose numeric columns contain non-numeric values. `data_processor.py` removes duplicates, handles missing values, and removes outliers (IQR or z-score) for whichever steps are enabled in `config/config.yaml`, and it also builds a cleaning report. `data_output.py` writes the cleaned data to CSV, creating the output folder if needed, and `utils.py` holds the shared logging setup and file validation. Because the column names and cleaning options live in the config, the same code can clean a different compatible CSV just by editing `config/config.yaml`.

## Run it

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

## Example output

```text
12:35:52 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, config=config/config.yaml, output=output/clean.csv
12:35:52 INFO     src.utils — Input file validated: fixtures/sample_data.csv
12:35:52 INFO     src.utils — Input file validated: config/config.yaml
12:35:52 INFO     src.data_loaders — Loaded CSV file: fixtures\sample_data.csv (100 rows)
12:35:52 INFO     src.data_loaders — Loaded YAML file: config\config.yaml
12:35:52 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
12:35:52 DEBUG    src.data_validator — Validation: 100 -> 98 rows (2 removed)
12:35:52 INFO     __main__ — Validation complete: 100 -> 98 rows
12:35:53 DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows
12:35:53 DEBUG    src.data_processor — handle_missing: 96 -> 94 rows
12:35:53 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, lower=43.625, upper=106.625, removed=2
12:35:53 INFO     __main__ — Processing complete: 98 -> 92 rows
12:35:53 DEBUG    src.data_output — Saved 92 rows to output\clean.csv
12:35:53 INFO     __main__ — Saved cleaned data to output\clean.csv

Cleaning report:
{
    'rows_before': 98,
    'rows_after': 92,
    'rows_removed': 6,
    'columns_before': 5,
    'columns_after': 5,
    'columns_removed': 0
}
```
