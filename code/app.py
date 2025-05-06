import argparse
import calendar
import os
import pandas as pd
import shutil
import warnings
import zipfile
from collections import Counter
from datetime import datetime
from gtfs import Gtfs, load
from trip import Trip
from enums import Emoji
from utils import format_total_seconds, get_abbr_day, sort_days

warnings.simplefilter('ignore', category=pd.errors.DtypeWarning) # Suppress DtypeWarnings from pandas

parser = argparse.ArgumentParser()
parser.add_argument('data', help='The name of the directory containing the GTFS data')
parser.add_argument('--info', action='store_true', help='Include a table of new/removed trips for each route in the report (optional)')
args = parser.parse_args()

def load_data() -> tuple[Gtfs, Gtfs]:
  datasets = []
  dir = os.path.join('..', 'data', args.data)
  for filename in os.listdir(dir):
    filepath = os.path.join(dir, filename)
    if filename.endswith('.zip'):
        basename = os.path.splitext(filename)[0]
        extract_dir = os.path.join(dir, basename)
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        gtfs = load(extract_dir)
        datasets.append(gtfs)
        try:
          shutil.rmtree(extract_dir)
        except Exception as e:
          print(f"Error deleting {extract_dir}: {e}")
  
  before = datasets[0]
  after = datasets[0]
  for gtfs in datasets:
    if gtfs.feed_info.feed_start_date < before.feed_info.feed_start_date:
      before = gtfs
    if gtfs.feed_info.feed_start_date > after.feed_info.feed_start_date:
      after = gtfs
  return before, after

def join_days(days: list[str]) -> str:
  if not days:
    return ''
  if len(days) == 1:
    return days[0]
  return ', '.join(days[:-1]) + ' and ' + days[-1]

def summarise_days_count(trips: list[Trip], days_count: dict[str, int], new: bool, file):
  for day in sort_days(days_count.keys()):
      count = days_count[day]
      x = count if count < len(trips) else 'All'
      y = 'ran' if not new else ('runs' if count == 1 else 'run')
      print(f"\t- {x} {y} on {day}", file=file)

def summarise_impacted_days(days_count: dict[str, int], file):
  if days_count:
    impacted_value = max(days_count.values())
    impacted_days = sort_days([k for k, v in days_count.items() if v == impacted_value])
    if impacted_days != list(calendar.day_name): # Only report days if some are impacted more than others
      days = join_days(impacted_days)
      if impacted_days == list(calendar.day_name)[:5]:
        days = 'Weekdays'
      if impacted_days == list(calendar.day_name)[5:]:
        days = 'Weekends'
      x = 'was' if len(impacted_days) == 1 else 'were'
      print(f"- {Emoji.CALENDAR.value} {days} {x} impacted the most", file=file)

def summarise_trips(gtfs: Gtfs, trips: list[Trip], new: bool, file):
  emoji = Emoji.WHITE_CHECK_MARK.value if new else Emoji.X.value
  if not trips:
    print(f"- {emoji} No {'new trips' if new else 'trips removed'}", file=file)
  else:
    trip_ids = [trip.trip_id for trip in trips]
    average_duration = format_total_seconds(gtfs.get_average_duration(trip_ids))
    days_count = gtfs.get_days_count(trips)
    x = 'new trips' if new else 'trips removed'
    print(f"- {emoji} {len(trips)} {x} with an average duration of {average_duration}", file=file)
    summarise_days_count(trips, days_count, new, file)

def info(gtfs: Gtfs, trips: list[Trip], file):
  print('||Trip|Headsign|Departure time|Duration|Days|', file=file)
  print('|--:|:--|:--|--:|--:|:--|', file=file)
  count = 0
  for trip in sorted(trips, key=lambda trip: trip.sort_key()):
    count += 1
    trip_id = trip.trip_id
    trip_headsign = trip.trip_headsign if trip.trip_headsign else '—'
    departure_time = format_total_seconds(gtfs.get_trip_departure_time(trip_id))
    duration = format_total_seconds(gtfs.get_trip_duration(trip_id))
    days = gtfs.get_days(trip)
    days_str = ', '.join(get_abbr_day(day) for day in days) if days else '—'
    print(f"|{count}|{trip_id}|{trip_headsign}|{departure_time}|{duration}|{days_str}|", file=file)

def main():
  start = datetime.now()
  filepath = os.path.join('..', 'output', f"{args.data}.md")
  with open(filepath, 'w', encoding='utf-8') as file:
    before, after = load_data()
    print(f"# {before.get_name()} {before.feed_info.feed_start_date} vs. {after.get_name()} {after.feed_info.feed_start_date}", file=file)
    
    routes = [v for k, v in before.routes.items() if k not in after.routes.keys()] # Removed Routes
    routes += after.routes.values() # All Routes
    for route in sorted(routes, key=lambda route: route.sort_key()):
      route_id = route.route_id
      route_long_name = f"| {route.route_long_name}" if route.route_long_name else ''
      route_type = route.route_type
      
      trips_before = before.get_trips(route_id)
      trips_after = after.get_trips(route_id)
      
      new_trips = [v for k, v in trips_after.items() if k not in trips_before.keys()] # New Trips are in after Gtfs
      removed_trips = [v for k, v in trips_before.items() if k not in trips_after.keys()] # Removed Trips are in before Gtfs

      # Skip routes without new or removed trips
      if new_trips or removed_trips:
        print(f"Processing {route_id} {route_long_name}")
        print(f"## {route_type.get_emoji().value} {route_id} {route_long_name}", file=file)
        if not trips_before:
          new_trip_ids = [trip.trip_id for trip in new_trips]
          average_duration = format_total_seconds(after.get_average_duration(new_trip_ids))
          days_count = after.get_days_count(new_trips)
          print(f"- {Emoji.WHITE_CHECK_MARK.value} All new trips with an average duration of {average_duration}", file=file)
          summarise_impacted_days(days_count, file)
          summarise_days_count(new_trips, days_count, True, file)
        elif not trips_after:
          days_count = before.get_days_count(removed_trips)
          print(f"- {Emoji.X.value} All trips removed", file=file)
          summarise_impacted_days(days_count, file)
          summarise_days_count(removed_trips, days_count, False, file)
        else:
          trips_emoji = Emoji.ARROW_UP.value if len(trips_before) < len(trips_after) else Emoji.ARROW_DOWN.value
          trips_value = abs(len(trips_before) - len(trips_after))
          
          x = before.get_average_duration(trips_before.keys())
          y = after.get_average_duration(trips_after.keys())
          average_duration_emoji = Emoji.ARROW_UP.value if x < y else Emoji.ARROW_DOWN.value
          average_duration_value = abs(x - y)
          
          days_count = dict(Counter(after.get_days_count(new_trips)) + Counter(before.get_days_count(removed_trips)))

          if trips_value:
            print(f"- Trip numbers {trips_emoji} {trips_value} from {len(trips_before)} to {len(trips_after)}", file=file)
          else:
            print('- Trip numbers did not change', file=file)
          if average_duration_value:
            print(f"- Average duration {average_duration_emoji} {format_total_seconds(average_duration_value)} overall from {format_total_seconds(x)} to {format_total_seconds(y)}", file=file)
          else:
            print('- Average duration did not change', file=file)
          summarise_impacted_days(days_count, file)
          summarise_trips(after, new_trips, True, file)
          summarise_trips(before, removed_trips, False, file)
        
        if new_trips and args.info:
          print(f"### {Emoji.WHITE_CHECK_MARK.value} New trips", file=file)
          info(after, new_trips, file)
        if removed_trips and args.info:
          print(f"### {Emoji.X.value} Removed trips", file=file)
          info(before, removed_trips, file)
  
  end = datetime.now()
  elapsed = end - start
  print(f"Completed in {format_total_seconds(elapsed.total_seconds())}")

main()