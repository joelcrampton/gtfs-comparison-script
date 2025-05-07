# GTFS Comparison Script
Public transport data is large and complex. When it changes, it can be difficult to predict how the network will be impacted. This is a Python script that compares two GTFS datasets and produces a report. Data must follow the official [GTFS specification](https://gtfs.org/documentation/schedule/reference/). See [`data/`](https://github.com/joelcrampton/gtfs-comparison-script/tree/main/data) for example data and [`output/`](https://github.com/joelcrampton/gtfs-comparison-script/tree/main/output) for example reports. The following GTFS files are required:
- [agency.txt](https://gtfs.org/documentation/schedule/reference/#agencytxt)
- [stops.txt](https://gtfs.org/documentation/schedule/reference/#stopstxt)
- [routes.txt](https://gtfs.org/documentation/schedule/reference/#routestxt)
- [trips.txt](https://gtfs.org/documentation/schedule/reference/#tripstxt)
- [stop_times.txt](https://gtfs.org/documentation/schedule/reference/#stop_timestxt)
- [calendar.txt](https://gtfs.org/documentation/schedule/reference/#calendartxt) or [calendar_dates.txt](https://gtfs.org/documentation/schedule/reference/#calendar_datestxt)
- [feed_info.txt](https://gtfs.org/documentation/schedule/reference/#feed_infotxt)

## 🖥 Requirements
- [Python](https://www.python.org/downloads/) 3.10.0 or later
- Install dependencies `pip install requirements.txt`

## ▶️ Run
### Manual
1. Clone the repository `git clone https://github.com/joelcrampton/gtfs-comparison-script.git`
2. Open a new terminal at `code/`
3. Copy a directory containing two GTFS datasets into `data/`. Datasets must be `.zip` files. The directory name must only include; alphanumeric characters, underscores and hyphens
4. Run the Python script e.g. `python app.py data --info`
    - `data` = the name of the directory containing the two GTFS datasets e.g. `boston`
    - `--info` = flag to include tables of new/removed trips for each route in the report (optional)
5. The Python script will take anywhere from a minute to 10+ minutes depending on the size of the GTFS data
6. A Markdown report will be created in `output/`. Only routes with new/removed trips will be included. Open in any Markdown compatible editor for best results e.g. Google Docs. Use the outline to jump between sections quickly
### GitHub actions
_Must be a contributor of this repository_
1. Create/select the desired branch
2. Copy a directory containing two GTFS datasets into `data/`. Datasets must be `.zip` files. The directory name must only include; alphanumeric characters, underscores and hyphens
3. Run the [ci-manual-run-python-script](https://github.com/joelcrampton/gtfs-comparison-script/actions/workflows/ci-manual-run-python-script.yaml) workflow
    - Select the branch
        - If `main` is selected, the workflow will:
            - Checkout to a `feature/data` branch
            - Push the report there
            - Create a pull request from `feature/data` to `main`
        - This is to avoid pushing directly to `main`
    - Data = the name of the directory containing the two GTFS datasets e.g. `boston`
    - Check box to include tables of new/removed trips for each route in the report
4. The workflow will take anywhere from a minute to 10+ minutes depending on the size of the GTFS data
5. A Markdown report will be created in `output/`. Only routes with new/removed trips will be included. Open in any Markdown compatible editor for best results e.g. Google Docs. Use the outline to jump between sections quickly

## 📌 Additional information
- Currently, new/removed trips are determined by `trip_id`. If a `trip_id` is in the new GTFS data, but not in the old, then is it considered to be new. If a `trip_id` is in the old GTFS data, but not in the new, then is it considered to be removed
- There are additional ways to determine new/removed trips e.g. `stop_id` sequence, trip duration or departure time. These will be investigated in the future...
