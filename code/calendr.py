import pandas as pd
from dataclasses import dataclass
from datetime import date, datetime
from utils import sort_days

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
        days['Monday'] = bool(row.get('monday')) if not pd.isna(row.get('monday')) else None
        days['Tuesday'] = bool(row.get('tuesday')) if not pd.isna(row.get('tuesday')) else None
        days['Wednesday'] = bool(row.get('wednesday')) if not pd.isna(row.get('wednesday')) else None
        days['Thursday'] = bool(row.get('thursday')) if not pd.isna(row.get('thursday')) else None
        days['Friday'] = bool(row.get('friday')) if not pd.isna(row.get('friday')) else None
        days['Saturday'] = bool(row.get('saturday')) if not pd.isna(row.get('saturday')) else None
        days['Sunday'] = bool(row.get('sunday')) if not pd.isna(row.get('sunday')) else None
        start_date = datetime.strptime(str(row.get('start_date')), '%Y%m%d').date() if not pd.isna(row.get('start_date')) else None
        end_date = datetime.strptime(str(row.get('end_date')), '%Y%m%d').date() if not pd.isna(row.get('end_date')) else None

        if service_id is None:
            raise ValueError('Missing service_id')
        for day in days.keys():
            if days[day] is None:
                raise ValueError(f"Missing {day.lower()}")
        if start_date is None:
            raise ValueError('Missing start_date')
        if end_date is None:
            raise ValueError('Missing end_date')
        
        return self(service_id, days, start_date, end_date)
    
    def get_id(self) -> str:
        return self.service_id
    
    def get_days(self) -> set[str]:
        return sort_days([k for k, v in self.days.items() if v])