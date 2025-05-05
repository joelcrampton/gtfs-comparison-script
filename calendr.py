import pandas as pd
from dataclasses import dataclass
from datetime import date, datetime
from enums import Day

# Reference: https://gtfs.org/documentation/schedule/reference/#calendartxt
@dataclass(frozen=True)
class Calendar:
    service_id: str # Required
    days: dict # Required
    start_date: date # Required
    end_date: date # Required

    @classmethod
    def from_series(self, row: pd.Series):
        service_id = str(row.get('service_id')) if not pd.isna(row.get('service_id')) else None
        days = {}
        days[Day.MONDAY] = bool(row.get('monday')) if not pd.isna(row.get('monday')) else None
        days[Day.TUESDAY] = bool(row.get('tuesday')) if not pd.isna(row.get('tuesday')) else None
        days[Day.WEDNESDAY] = bool(row.get('wednesday')) if not pd.isna(row.get('wednesday')) else None
        days[Day.THURSDAY] = bool(row.get('thursday')) if not pd.isna(row.get('thursday')) else None
        days[Day.FRIDAY] = bool(row.get('friday')) if not pd.isna(row.get('friday')) else None
        days[Day.SATURDAY] = bool(row.get('saturday')) if not pd.isna(row.get('saturday')) else None
        days[Day.SUNDAY] = bool(row.get('sunday')) if not pd.isna(row.get('sunday')) else None
        start_date = datetime.strptime(str(row.get('start_date')), '%Y%m%d').date() if not pd.isna(row.get('start_date')) else None
        end_date = datetime.strptime(str(row.get('end_date')), '%Y%m%d').date() if not pd.isna(row.get('end_date')) else None

        if service_id is None:
            raise ValueError('Missing service_id')
        for day in days.keys():
            if days[day] is None:
                raise ValueError("Missing {day.name.lower()}")
        if start_date is None:
            raise ValueError('Missing start_date')
        if end_date is None:
            raise ValueError('Missing end_date')
        
        return self(service_id, days, start_date, end_date)
    
    def get_id(self) -> str:
        return self.service_id
    
    def get_available_days(self) -> set[Day]:
        return [k for k, v in self.days.items() if v]

    def get_unavailable_days(self) -> set[Day]:
        return [k for k, v in self.days.items() if not v]