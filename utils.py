import re
from datetime import time, timedelta
from email_validator import validate_email, EmailNotValidError
from urllib.parse import urlparse

def adjust_time(t: str) -> time:
   h, m, s = map(int, t.split(":"))
   h = h % 24  # Normalise the hour
   return time(int(h), int(m), int(s))

def check_color(color: str) -> bool:
    return bool(re.fullmatch(r'[0-9a-fA-F]{6}', color))

def check_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme and parsed.netloc

def check_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def get_average_duration(durations: list) -> timedelta:
    total_seconds = 0
    for t in durations:
      total_seconds += t.total_seconds()
    if total_seconds == 0:
      return timedelta()
    average_seconds = total_seconds / len(durations)
    h, m, s = split_total_seconds(average_seconds)
    return timedelta(hours=h, minutes=m, seconds=s)

def get_int_prefix(x: str):
    match = re.match(r'^(\d+)', x)
    return int(match.group(1)) if match else None

def get_time_diff(x: timedelta, y: timedelta) -> timedelta:
  elapsed = abs(x.total_seconds() - y.total_seconds())
  h, m, s = split_total_seconds(elapsed)
  return timedelta(hours=h, minutes=m, seconds=s)

def format_timedelta(t: timedelta) -> str:
  h, m, s = split_total_seconds(t.total_seconds())
  return f'{int(h)}:{int(m):02}:{int(s):02}'

def split_total_seconds(total_seconds: float) -> tuple[float, float, float]:
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return h, m, s