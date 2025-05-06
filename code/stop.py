import pandas as pd
from dataclasses import dataclass
from enums import LocationType, WheelchairAccess
from utils import check_url

# Reference: https://gtfs.org/documentation/schedule/reference/#stopstxt
@dataclass(frozen=True)
class Stop:
    stop_id: str # Required
    stop_code: str # Optional
    stop_name: str # Conditionally Required
    tts_stop_name: str # Optional
    stop_desc: str # Optional
    stop_lat: float # Conditionally Required
    stop_lon: float # Conditionally Required
    zone_id: str # Optional
    stop_url: str # Optional
    location_type: LocationType # Optional
    parent_station: str # Conditionally Required
    stop_timezone: str # Optional
    wheelchair_boarding: WheelchairAccess # Optional
    level_id: str # Optional
    platform_code: str # Optional

    @classmethod
    def from_series(self, row: pd.Series):
        stop_id = str(row.get('stop_id')) if not pd.isna(row.get('stop_id')) else None
        stop_code = str(row.get('stop_code')) if not pd.isna(row.get('stop_code')) else None
        stop_name = str(row.get('stop_name')) if not pd.isna(row.get('stop_name')) else None
        tts_stop_name = str(row.get('tts_stop_name')) if not pd.isna(row.get('tts_stop_name')) else None
        stop_desc = str(row.get('stop_desc')) if not pd.isna(row.get('stop_desc')) else None
        stop_lat = float(row.get('stop_lat')) if not pd.isna(row.get('stop_lat')) else None
        stop_lon = float(row.get('stop_lon')) if not pd.isna(row.get('stop_lon')) else None
        zone_id = str(row.get('zone_id')) if not pd.isna(row.get('zone_id')) else None
        stop_url = str(row.get('stop_url')) if check_url(str(row.get('stop_url'))) else None
        location_type = LocationType(row.get('location_type')) if not pd.isna(row.get('location_type')) else LocationType.STOP
        parent_station = str(row.get('parent_station')) if not pd.isna(row.get('parent_station')) else None
        stop_timezone = str(row.get('stop_timezone')) if not pd.isna(row.get('stop_timezone')) else None
        wheelchair_boarding = WheelchairAccess(row.get('wheelchair_boarding')) if not pd.isna(row.get('wheelchair_boarding')) else WheelchairAccess.NO_INFORMATION
        level_id = str(row.get('level_id')) if not pd.isna(row.get('level_id')) else None
        platform_code = str(row.get('platform_code')) if not pd.isna(row.get('platform_code')) else None
        
        if stop_id is None:
            raise ValueError('Missing stop_id')

        return self(stop_id, stop_code, stop_name, tts_stop_name, stop_desc, stop_lat, stop_lon, zone_id, stop_url, location_type, parent_station, stop_timezone, wheelchair_boarding, level_id, platform_code)
    
    def get_id(self) -> str:
        return self.stop_id