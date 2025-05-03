import pandas as pd
from dataclasses import dataclass
from datetime import date, datetime
from enums import ExceptionType

# Reference: https://gtfs.org/documentation/schedule/reference/#calendar_datestxt
@dataclass(frozen=True)
class CalendarDate:
    service_id: str # Required
    service_date: date # Required
    exception_type: ExceptionType # Required

    @classmethod
    def from_series(self, row: pd.Series):
        service_id = str(row.get('service_id')) if not pd.isna(row.get('service_id')) else None
        service_date = datetime.strptime(str(row.get('date')), '%Y%m%d').date() if not pd.isna(row.get('date')) else None
        exception_type = ExceptionType(row.get('exception_type')) if not pd.isna(row.get('exception_type')) else None

        if service_id is None:
            raise ValueError('Missing service_id')
        if service_date is None:
            raise ValueError('Missing date')
        if exception_type is None:
            raise ValueError('Missing exception_type')
        
        return self(service_id, service_date, exception_type)
    
    def get_id(self) -> str:
        return self.service_id