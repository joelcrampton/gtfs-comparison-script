import os
import pandas as pd
from dataclasses import dataclass
from agency import Agency
from stop import Stop
from route import Route
from trip import Trip
from stop_time import StopTime
from calendr import Calendar
from calendar_date import CalendarDate
from shape import Shape
from feed_info import FeedInfo
from enums import RouteType

@dataclass(frozen=True)
class Gtfs:
  agencies: dict[str, Agency]
  stops: dict[str, Stop]
  routes: dict[str, Route]
  trips: dict[str, Trip]
  stop_times: dict[str, list[StopTime]]
  calendars: dict[str, Calendar]
  calendar_dates: dict[str, CalendarDate]
  shapes: dict[str, list[Shape]]
  feed_info: FeedInfo

  def summary(self):
    summary = f"{self.feed_info.feed_publisher_name} {self.feed_info.feed_start_date}: "
    summary += f"\n\t{len(self.agencies)} agencies"
    summary += f"\n\t{len(self.stops)} stops"
    summary += f"\n\t{len(self.routes)} routes"
    summary += f"\n\t{len(self.trips)} trips"
    summary += f"\n\t{sum(len(v) for v in self.stop_times.values())} stop_times"
    summary += f"\n\t{len(self.calendars)} calendars"
    summary += f"\n\t{len(self.calendar_dates)} calendar_dates"
    summary += f"\n\t{sum(len(v) for v in self.shapes.values())} shapes"
    return summary
  
  def get_route_types(self) -> set[RouteType]:
    return sorted({route.route_type for route in self.routes})

  def get_trips(self, route_id: str) -> dict[str, Trip]:
    return {k: v for k, v in self.trips.items() if v.route_id == route_id}
  
  def get_trip_departure_time(self, trip_id: str) -> int:
    stop_times = self.stop_times[trip_id]
    departure_stop_time = min(stop_times, key=lambda stop_time: stop_time.stop_sequence)
    return departure_stop_time.departure_time

  def get_trip_arrival_time(self, trip_id: str) -> int:
    stop_times = self.stop_times[trip_id]
    arrival_stop_time = max(stop_times, key=lambda stop_time: stop_time.stop_sequence)
    return arrival_stop_time.arrival_time

  def get_trip_duration(self, trip_id: str) -> int:
    departure_time = self.get_trip_departure_time(trip_id)
    arrival_time = self.get_trip_arrival_time(trip_id)
    return arrival_time - departure_time
    
  def get_average_duration(self, trip_ids: list[str]) -> int:
    total_seconds = 0
    for trip_id in trip_ids:
      total_seconds += self.get_trip_duration(trip_id)
    return total_seconds // len(trip_ids)

  def get_days(self, trip: Trip) -> list[str]:
    service_id = trip.service_id
    # calendars.txt is ideal
    if self.calendars:
      return self.calendars[service_id].get_days()
    # calenar_dates.txt as an alternative
    elif self.calendar_dates:
      calendar_date = self.calendar_dates[service_id]
      return [calendar_date.get_day()]
    return []

  def get_days_count(self, trips: list[Trip]) -> dict[str, int]:
    count = {}
    for trip in trips:
      days = self.get_days(trip)
      for day in days:
        count[day] = count[day] + 1 if day in count else 1
    return count

  def get_name(self) -> str:
    if self.feed_info.feed_publisher_name == 'Tool Generated':
      return list(self.agencies.values())[0].agency_name
    return self.feed_info.feed_publisher_name

def load_dict_value(df: pd.DataFrame, type_: type) -> dict:
  collection = {}
  for _, row in df.iterrows():
    obj = type_.from_series(row)
    collection[obj.get_id()] = obj
  return collection

def load_dict_list(df: pd.DataFrame, type_: type) -> dict:
  collection = {}
  for _, row in df.iterrows():
    obj = type_.from_series(row)
    id = obj.get_id()
    if id in collection:
      collection[id].append(obj)
    else:
      collection[id] = [obj]
  return collection

def load(dir) -> Gtfs:
  filepath = f"{dir}/agency.txt"
  print(f"Loading {filepath}")
  agencies = load_dict_value(pd.read_csv(filepath), Agency)
  
  filepath = f"{dir}/stops.txt"
  print(f"Loading {filepath}")
  stops = load_dict_value(pd.read_csv(filepath), Stop)
  
  filepath = f"{dir}/routes.txt"
  print(f"Loading {filepath}")
  routes = load_dict_value(pd.read_csv(filepath), Route)
  
  filepath = f"{dir}/trips.txt"
  print(f"Loading {filepath}")
  trips = load_dict_value(pd.read_csv(filepath), Trip)
  
  filepath = f"{dir}/stop_times.txt"
  print(f"Loading {filepath}")
  stop_times = load_dict_list(pd.read_csv(filepath), StopTime)
  
  filepath = f"{dir}/calendar.txt"
  if os.path.exists(filepath):
    print(f"Loading {filepath}")
    calendars = load_dict_value(pd.read_csv(filepath), Calendar)
  else:
    calendars = {}
  
  filepath = f"{dir}/calendar_dates.txt"
  if os.path.exists(filepath):
    print(f"Loading {filepath}")
    calendar_dates = load_dict_value(pd.read_csv(filepath), CalendarDate)
  else:
    calendar_dates = {}
  
  filepath = f"{dir}/shapes.txt"
  print(f"Loading {filepath}")
  shapes = load_dict_list(pd.read_csv(filepath), Shape)
  
  filepath = f"{dir}/feed_info.txt"
  print(f"Loading {filepath}")
  feed_info = FeedInfo.from_series(pd.read_csv(filepath).iloc[0])
  
  return Gtfs(agencies, stops, routes, trips, stop_times, calendars, calendar_dates, shapes, feed_info)