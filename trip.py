import pandas as pd
from dataclasses import dataclass
from enums import BikesAllowed, DirectionId, WheelchairAccess
from utils import get_int_prefix

# Reference: https://gtfs.org/documentation/schedule/reference/#tripstxt
@dataclass(frozen=True)
class Trip:
    route_id: str # Required
    service_id: str # Required
    trip_id: str # Required
    trip_headsign: str # Optional
    trip_short_name: str # Optional
    direction_id: DirectionId # Optional
    block_id: str # Optional
    shape_id: str # Conditionally Required
    wheelchair_accessible: WheelchairAccess # Optional
    bikes_allowed: BikesAllowed # Optional

    @classmethod
    def from_series(self, row: pd.Series):
        route_id = str(row.get('route_id')) if not pd.isna(row.get('route_id')) else None
        service_id = str(row.get('service_id')) if not pd.isna(row.get('service_id')) else None
        trip_id = str(row.get('trip_id')) if not pd.isna(row.get('trip_id')) else None
        trip_headsign = str(row.get('trip_headsign')) if not pd.isna(row.get('trip_headsign')) else None
        trip_short_name = str(row.get('trip_short_name')) if not pd.isna(row.get('trip_short_name')) else None
        direction_id = DirectionId(row.get('direction_id')) if not pd.isna(row.get('direction_id')) else None
        block_id = str(row.get('block_id')) if not pd.isna(row.get('block_id')) else None
        shape_id = str(row.get('shape_id')) if not pd.isna(row.get('shape_id')) else None
        wheelchair_accessible = WheelchairAccess(row.get('wheelchair_accessible')) if not pd.isna(row.get('wheelchair_accessible')) else WheelchairAccess.NO_INFORMATION
        bikes_allowed = BikesAllowed(row.get('bikes_allowed')) if not pd.isna(row.get('bikes_allowed')) else BikesAllowed.NO_INFORMATION
        
        if route_id is None:
            raise ValueError('Missing route_id')
        if service_id is None:
            raise ValueError('Missing service_id')
        if trip_id is None:
            raise ValueError('Missing trip_id')

        return self(route_id, service_id, trip_id, trip_headsign, trip_short_name, direction_id, block_id, shape_id, wheelchair_accessible, bikes_allowed)
    
    def get_id(self) -> str:
        return self.trip_id

    def sort_key(self):
        prefix = get_int_prefix(self.trip_id)
        return (0, prefix) if prefix is not None else (1, self.trip_id)