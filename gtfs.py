import pandas as pd
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from agency import Agency
from stop import Stop
from route import Route
from trip import Trip
from stop_time import StopTime
from calendr import Calendar
from calendar_date import CalendarDate
from shape import Shape
from feed_info import FeedInfo
from enums import Day, RouteType
from utils import find_average_duration

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
    summary = f'{self.feed_info.feed_publisher_name} {self.feed_info.feed_start_date}: '
    summary += f'\n\t{len(self.agencies)} agencies, '
    summary += f'\n\t{len(self.stops)} stops, '
    summary += f'\n\t{len(self.routes)} routes, '
    summary += f'\n\t{len(self.trips)} trips, '
    summary += f'\n\t{sum(len(v) for v in self.stop_times.values())} stop_times, '
    summary += f'\n\t{len(self.calendars)} calendars, '
    summary += f'\n\t{len(self.calendar_dates)} calendar_dates, '
    summary += f'\n\t{sum(len(v) for v in self.shapes.values())} shapes'
    return summary
  
  def get_route_types(self) -> set[RouteType]:
    return sorted({route.route_type for route in self.routes})

  def get_trips(self, route_id: str) -> dict[str, Trip]:
    return {k: v for k, v in self.trips.items() if v.route_id == route_id}
  
  def get_trip_start_time(self, trip_id: str) -> time:
    stop_times = self.stop_times[trip_id]
    start_stop_time = min(stop_times, key=lambda stop_time: stop_time.stop_sequence)
    return start_stop_time.arrival_time

  def get_trip_end_time(self, trip_id: str) -> time:
    stop_times = self.stop_times[trip_id]
    end_stop_time = max(stop_times, key=lambda stop_time: stop_time.stop_sequence)
    return end_stop_time.departure_time

  def get_trip_duration(self, trip_id: str) -> timedelta:
    start_time = datetime.combine(datetime.today(), self.get_trip_start_time(trip_id))
    end_time = datetime.combine(datetime.today(), self.get_trip_end_time(trip_id))
    if end_time < start_time:
      end_time += timedelta(days=1) # Account for next day
    return end_time - start_time
    
  def get_average_duration(self, trips: list[Trip]) -> timedelta:
    durations = []
    for trip in trips:
      durations.append(self.get_trip_duration(trip.trip_id))
    return find_average_duration(durations)
  
  def get_available_days(self, service_id: str) -> list:
    return self.calendars[service_id].get_available_days()

  def get_available_days_count(self, trips: list[Trip]) -> dict[Day, int]:
    count = {}
    for trip in trips:
      service_id = trip.service_id
      days = self.get_available_days(service_id)
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
  filepath = f'{dir}/agency.txt'
  print(f'Loading {filepath}')
  agencies = load_dict_value(pd.read_csv(filepath).sort_values(by='agency_name'), Agency)
  
  filepath = f'{dir}/stops.txt'
  print(f'Loading {filepath}')
  stops = load_dict_value(pd.read_csv(filepath).sort_values(by='stop_id'), Stop)
  
  filepath = f'{dir}/routes.txt'
  print(f'Loading {filepath}')
  routes = load_dict_value(pd.read_csv(filepath).sort_values(by='route_id'), Route)
  
  filepath = f'{dir}/trips.txt'
  print(f'Loading {filepath}')
  trips = load_dict_value(pd.read_csv(filepath).sort_values(by='trip_id'), Trip)
  
  filepath = f'{dir}/stop_times.txt'
  print(f'Loading {filepath}')
  stop_times = load_dict_list(pd.read_csv(filepath).sort_values(by=['trip_id', 'stop_id']), StopTime)
  
  filepath = f'{dir}/calendar.txt'
  print(f'Loading {filepath}')
  calendars = load_dict_value(pd.read_csv(filepath).sort_values(by='service_id'), Calendar)
  
  filepath = f'{dir}/calendar_dates.txt'
  print(f'Loading {filepath}')
  calendar_dates = load_dict_value(pd.read_csv(filepath).sort_values(by='service_id'), CalendarDate)
  
  filepath = f'{dir}/shapes.txt'
  print(f'Loading {filepath}')
  shapes = load_dict_list(pd.read_csv(filepath).sort_values(by='shape_id'), Shape)
  
  filepath = f'{dir}/feed_info.txt'
  print(f'Loading {filepath}')
  feed_info = FeedInfo.from_series(pd.read_csv(filepath).iloc[0])
  
  return Gtfs(agencies, stops, routes, trips, stop_times, calendars, calendar_dates, shapes, feed_info)