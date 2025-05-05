import re
from email_validator import validate_email, EmailNotValidError
from urllib.parse import urlparse

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

def get_int_prefix(x: str):
    match = re.match(r'^(\d+)', x)
    return int(match.group(1)) if match else None

def get_total_seconds(t: str) -> int:
   h, m, s = map(int, t.split(":"))
   return h * 3600 + m * 60 + s

def format_total_seconds(total_seconds) -> str:
    total_seconds = int(total_seconds)
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h}:{m:02}:{s:02}"
