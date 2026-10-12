# MP1 Data Pipeline

This project is a command-line data pipeline that loads a CSV file, validates it, cleans it, and saves the result, with every cleaning decision controlled by a YAML configuration file instead of hard-coded values. Data moves through the pipeline in four stages: load, validate, process, and save. `pipeline.py` is the entry point; it parses the command-line arguments, checks that the input and config files exist, and coordinates the other modules. The reusable code lives in the `src/` package. `data_loaders.py` reads CSV, JSON, and YAML files based on their extension, and `data_validator.py` checks that the required columns exist and removes rows whose numeric columns contain non-numeric values. `data_processor.py` removes duplicates, handles missing values, and removes outliers (IQR or z-score) for whichever steps are enabled in `config/config.yaml`, and it also builds a cleaning report. `data_output.py` writes the cleaned data to CSV, creating the output folder if needed, and `utils.py` holds the shared logging setup and file validation. Because the column names and cleaning options live in the config, the same code can clean a different compatible CSV just by editing `config/config.yaml`.

## Run it

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

## Example output

```text
PASTE THE OUTPUT FROM YOUR OWN RUN OF THE COMMAND ABOVE HERE
```
