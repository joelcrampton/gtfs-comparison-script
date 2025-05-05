# GTFS Comparison Script
This is a Python script that compares two GTFS datasets and produces a report. The following GTFS files are required; `agency.txt`, `stops.txt`, `routes.txt`, `trips.txt`, `stop_times.txt`, `calendar.txt`, `calendar_dates.txt`, `shapes.txt` and `feed_info.txt`. Documentation can be found at https://gtfs.org/documentation/schedule/reference/. See `data/` for example data and `output/` for example reports

## :desktop_computer: Requirements
- Python 3.10.0 or later
- `pip install email_validator pandas`

## :arrow_forward: Run
1. Clone the repository `git clone https://github.com/joelcrampton/gtfs-comparison-script.git`
2. Open a new terminal at `gtfs-comparison-script/`
3. Copy a directory containing two GTFS datasets into `data/`. Datasets must be `.zip` files. Name this directory after the region it is for
4. `python app.py region --info`
    - `region` = the name of the directory containing the GTFS data e.g. `boston`
    - `--info` = include a table of new/removed trips for each route in the report (optional)
5. The script will take approximately 5 minutes to complete depending on the size of the GTFS data
6. A report named `region.md` will be created in `output/`. Only routes with new/removed trips will be included. Open in any Markdown compatible editor for best results e.g. Google Docs. Use the Markdown outline to jump between sections quickly
