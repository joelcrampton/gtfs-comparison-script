# GTFS Comparison Script
Public transport data is complex and it can be difficult to notice the impact a network will might have. This is a Python script that compares two GTFS datasets and produces a report. Data must follow the official GTFS specification https://gtfs.org/documentation/schedule/reference/. See [`data/`](https://github.com/joelcrampton/gtfs-comparison-script/tree/main/data) for example data and [`output/`](https://github.com/joelcrampton/gtfs-comparison-script/tree/main/output) for example reports. The following GTFS files are required:
- `agency.txt`
- `stops.txt`
- `routes.txt`
- `trips.txt`
- `stop_times.txt`
- `calendar.txt` or `calendar_dates.txt`
- `feed_info.txt`

## 🖥 Requirements
- [Python](https://www.python.org/downloads/) 3.10.0 or later
- Install Python libraries `pip install email_validator pandas`

## ▶️ Run
1. Clone the repository `git clone https://github.com/joelcrampton/gtfs-comparison-script.git`
2. Open a new terminal at `gtfs-comparison-script/`
3. Copy a directory containing two GTFS datasets into [`data/`](https://github.com/joelcrampton/gtfs-comparison-script/tree/main/data). Datasets must be `.zip` files. Name this directory after the region it is for
4. Run the Python script e.g. `python app.py data --info`
    - `data` = the name of the directory containing the two GTFS datasets e.g. `boston`
    - `--info` = include a table of new/removed trips for each route in the report (optional)
5. The Python script will take anywhere from a few seconds to 10+ minutes to complete depending on the size of the GTFS data
6. A Markdown report will be created in [`output/`](https://github.com/joelcrampton/gtfs-comparison-script/tree/main/output). Only routes with new/removed trips will be included. Open in any Markdown compatible editor for best results e.g. Google Docs. Use the outline to jump between sections quickly
    - Currently, new/removed trips are determined by `trip_id`. If a `trip_id` is in the new GTFS data, but not in the old, then is it considered to be new. If a `trip_id` is in the old GTFS data, but not in the new, then is it considered to be removed
    - There are additional ways to determine new/removed trips e.g. `stop_id` sequence, trip duration or departure time. These will be investigated in the future...
