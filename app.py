import os
import pandas as pd
import shutil
import sys
import warnings
import zipfile
from collections import Counter
from datetime import datetime
from gtfs import Gtfs, load
from trip import Trip
from enums import Day, Emoji
from utils import format_total_seconds

warnings.simplefilter("ignore", category=pd.errors.DtypeWarning) # Suppress DtypeWarnings from pandas

DATA = sys.argv[1]
INFO = False
if len(sys.argv) > 2:
  if sys.argv[2] == '--info':
    INFO = True

def load_data() -> tuple[Gtfs, Gtfs]:
  datasets = []
  dir = os.path.join('data', DATA)
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
        shutil.rmtree(extract_dir)
  
  before = datasets[0]
  after = datasets[0]
  for gtfs in datasets:
    if gtfs.feed_info.feed_start_date < before.feed_info.feed_start_date:
      before = gtfs
    if gtfs.feed_info.feed_start_date > after.feed_info.feed_start_date:
      after = gtfs
  return before, after

def join_days(days: list[Day]) -> str:
  if not days:
    return ''
  if len(days) == 1:
    return days[0].name.title()
  return ', '.join(d.name.title() for d in days[:-1]) + ' and ' + days[-1].name.title()

def summarise_days_count(days_count: dict[Day, int], file):
  if not days_count:
    return
  impacted_value = max(days_count.values())
  impacted_days = sorted([k for k, v in days_count.items() if v == impacted_value])
  if set(impacted_days) != set(Day.get_week()): # Only report Days if some are impacted more than others
    days = join_days(impacted_days)
    if set(impacted_days) == set(Day.get_weekdays()):
      days = 'Weekdays'
    if set(impacted_days) == set(Day.get_weekends()):
      days = 'Weekends'
    print(f"- {Emoji.CALENDAR.value} {days} {'was' if len(impacted_days) == 1 else 'were'} impacted the most", file=file)

def summarise_trips(gtfs: Gtfs, trips: list[Trip], new: bool, file):
  emoji = Emoji.WHITE_CHECK_MARK.value if new else Emoji.X.value
  if not trips:
    print(f"- {emoji} No {'new trips' if new else 'trips removed'}", file=file)
  else:
    average_duration = gtfs.get_average_duration([trip.trip_id for trip in trips])
    available_days_count = gtfs.get_available_days_count([trip.service_id for trip in trips])
    print(f"- {emoji} {len(trips)} {'new trips' if new else 'trips removed'} with an average duration of {format_total_seconds(average_duration)}", file=file)
    for day in sorted(available_days_count.keys()):
      print(f"\t- {available_days_count[day]} on {day.name.title()}", file=file)

def info(gtfs: Gtfs, trips: list[Trip], file):
  print('||Trip|Headsign|Start time|Duration|Days|', file=file)
  print('|--:|:--|:--|--:|--:|:--|', file=file)
  count = 0
  for trip in sorted(trips, key=lambda trip: trip.sort_key()):
    count += 1
    service_id = trip.service_id
    trip_id = trip.trip_id
    trip_headsign = trip.trip_headsign if trip.trip_headsign else '—'
    start_time = format_total_seconds(gtfs.get_trip_start_time(trip_id))
    duration = format_total_seconds(gtfs.get_trip_duration(trip_id))
    days = gtfs.get_available_days(service_id)
    days = ', '.join(day.get_short_name().title() for day in days) if days else '—'
    print(f"|{count}|{trip_id}|{trip_headsign}|{start_time}|{duration}|{days}|", file=file)

def main():
  start = datetime.now()
  with open(f"output/{DATA}.md", 'w', encoding='utf-8') as file:
    before, after = load_data()
    print(f"# {before.get_name()} {before.feed_info.feed_start_date} vs. {after.get_name()} {after.feed_info.feed_start_date}", file=file)
    
    routes = [v for k, v in before.routes.items() if k not in after.routes.keys()] # Removed Routes
    routes += after.routes.values() # All Routes
    for route in sorted(routes, key=lambda route: route.sort_key()):
      route_id = route.route_id
      route_long_name = route.route_long_name
      route_type = route.route_type
      
      trips_before = before.get_trips(route_id)
      trips_after = after.get_trips(route_id)
      
      new_trips = [v for k, v in trips_after.items() if k not in trips_before.keys()] # New Trips are in after Gtfs
      removed_trips = [v for k, v in trips_before.items() if k not in trips_after.keys()] # Removed Trips are in before Gtfs
      new_service_ids = list({trip.service_id for trip in new_trips})
      removed_service_ids = list({trip.service_id for trip in removed_trips})

      # Skip routes without new or removed trips
      if new_trips or removed_trips:
        print(f"Processing {route_id} | {route_long_name}")
        print(f"## {route_type.get_emoji().value} {route_id} | {route_long_name}", file=file)
        if not trips_before:
          days_count = after.get_available_days_count(new_service_ids)
          print(f"- {Emoji.WHITE_CHECK_MARK.value} All new trips", file=file)
          summarise_days_count(days_count, file)
          for day in sorted(days_count.keys()):
            print(f"\t- {days_count[day]} on {day.name.title()}", file=file)
        elif not trips_after:
          days_count = before.get_available_days_count(removed_service_ids)
          print(f"- {Emoji.X.value} All trips removed", file=file)
          summarise_days_count(days_count, file)
          for day in sorted(days_count.keys()):
            print(f"\t- {days_count[day]} on {day.name.title()}", file=file)
        else:
          trips_emoji = Emoji.ARROW_UP.value if len(trips_before) < len(trips_after) else Emoji.ARROW_DOWN.value
          trips_value = abs(len(trips_before) - len(trips_after))
          
          x = before.get_average_duration(trips_before.keys())
          y = after.get_average_duration(trips_after.keys())
          average_duration_emoji = Emoji.ARROW_UP.value if x < y else Emoji.ARROW_DOWN.value
          average_duration_value = abs(x - y)
          days_count = dict(Counter(after.get_available_days_count(new_service_ids)) + Counter(before.get_available_days_count(removed_service_ids)))
          
          if trips_value:
            print(f"- Trip numbers {trips_emoji} {trips_value} from {len(trips_before)} to {len(trips_after)}", file=file)
          else:
            print('- Trip numbers did not change', file=file)
          if average_duration_value:
            print(f"- Average duration {average_duration_emoji} {format_total_seconds(average_duration_value)} overall from {format_total_seconds(x)} to {format_total_seconds(y)}", file=file)
          else:
            print('- Average duration did not change', file=file)
          summarise_days_count(days_count, file)
          summarise_trips(after, new_trips, True, file)
          summarise_trips(before, removed_trips, False, file)
        
        if new_trips and INFO:
          print(f"### {Emoji.WHITE_CHECK_MARK.value} New trips", file=file)
          info(after, new_trips, file)
        if removed_trips and INFO:
          print(f"### {Emoji.X.value} Removed trips", file=file)
          info(before, removed_trips, file)
  
  end = datetime.now()
  elapsed = end - start
  print(f"Completed in {format_total_seconds(elapsed.total_seconds())}")

main()