import pandas as pd
from dataclasses import dataclass
from utils import check_email, check_url

# Reference: https://gtfs.org/documentation/schedule/reference/#agencytxt
@dataclass(frozen=True)
class Agency:
    agency_id: str # Conditionally Required
    agency_name: str # Required
    agency_url: str # Required
    agency_timezone: str # Required
    agency_lang: str # Optional
    agency_phone: str # Optional
    agency_fare_url: str # Optional
    agency_email: str # Optional

    @classmethod
    def from_series(self, row: pd.Series):
        agency_id = str(row.get('agency_id')) if not pd.isna(row.get('agency_id')) else None
        agency_name = str(row.get('agency_name')) if not pd.isna(row.get('agency_name')) else None
        agency_url = str(row.get('agency_url')) if check_url(str(row.get('agency_url'))) else None
        agency_timezone = str(row.get('agency_timezone')) if not pd.isna(row.get('agency_timezone')) else None
        agency_lang = str(row.get('agency_lang')) if not pd.isna(row.get('agency_lang')) else None
        agency_phone = str(row.get('agency_phone')) if not pd.isna(row.get('agency_phone')) else None
        agency_fare_url = str(row.get('agency_fare_url')) if check_url(str(row.get('agency_fare_url'))) else None
        agency_email = str(row.get('agency_email')) if check_email(str(row.get('agency_email'))) else None

        if agency_name is None:
            raise ValueError('Missing agency_name')
        if agency_url is None:
            raise ValueError(f'Invalid agency_url \'{agency_url}\'')
        if agency_timezone is None:
            raise ValueError('Missing agency_timezone')
        
        return self(agency_id, agency_name, agency_url, agency_timezone, agency_lang, agency_phone, agency_fare_url, agency_email)
    
    def get_id(self) -> str:
        return self.agency_id if self.agency_id is not None else self.agency_name