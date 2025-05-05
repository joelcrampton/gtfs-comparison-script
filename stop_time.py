import pandas as pd
from dataclasses import dataclass
from enums import CollectionType, Continuous, Timepoint
from utils import get_total_seconds

# Reference: https://gtfs.org/documentation/schedule/reference/#stop_timestxt
@dataclass(frozen=True)
class StopTime:
    trip_id: str # Required
    arrival_time: int # Conditionally Required
    departure_time: int # Conditionally Required
    stop_id: str # Conditionally Required
    location_group_id: str # Conditionally Forbidden
    location_id: str # Conditionally Forbidden
    stop_sequence: int # Required
    stop_headsign: str # Optional
    start_pickup_drop_off_window: int # Conditionally Required
    end_pickup_drop_off_window: int # Conditionally Required
    pickup_type: CollectionType # Conditionally Forbidden
    drop_off_type: CollectionType # Conditionally Forbidden
    continuous_pickup: Continuous # Conditionally Forbidden
    continuous_drop_off: Continuous # Conditionally Forbidden
    shape_dist_traveled: float # Optional
    timepoint: Timepoint # Optional
    pickup_booking_rule_id: str # Optional
    drop_off_booking_rule_id: str # Optional

    @classmethod
    def from_series(self, row: pd.Series):
        trip_id = str(row.get('trip_id')) if not pd.isna(row.get('trip_id')) else None
        arrival_time = get_total_seconds(row.get('arrival_time')) if not pd.isna(row.get('arrival_time')) else None
        departure_time = get_total_seconds(row.get('departure_time')) if not pd.isna(row.get('departure_time')) else None
        stop_id = str(row.get('stop_id')) if not pd.isna(row.get('stop_id')) else None
        location_group_id = str(row.get('location_group_id')) if not pd.isna(row.get('location_group_id')) else None
        location_id = str(row.get('location_id')) if not pd.isna(row.get('location_id')) else None
        stop_sequence = int(row.get('stop_sequence')) if not pd.isna(row.get('stop_sequence')) else None
        stop_headsign = str(row.get('stop_headsign')) if not pd.isna(row.get('stop_headsign')) else None
        start_pickup_drop_off_window = get_total_seconds(row.get('start_pickup_drop_off_window')) if not pd.isna(row.get('start_pickup_drop_off_window')) else None
        end_pickup_drop_off_window = get_total_seconds(row.get('end_pickup_drop_off_window')) if not pd.isna(row.get('end_pickup_drop_off_window')) else None
        pickup_type = CollectionType(row.get('pickup_type')) if not pd.isna(row.get('pickup_type')) else CollectionType.REGULARY_SCHEDULED
        drop_off_type = CollectionType(row.get('drop_off_type')) if not pd.isna(row.get('drop_off_type')) else CollectionType.REGULARY_SCHEDULED
        continuous_pickup = Continuous(row.get('continuous_pickup')) if not pd.isna(row.get('continuous_pickup')) else Continuous.NO_CONTINUOUS
        continuous_drop_off = Continuous(row.get('continuous_drop_off')) if not pd.isna(row.get('continuous_drop_off')) else Continuous.NO_CONTINUOUS
        shape_dist_traveled = float(row.get('shape_dist_traveled')) if not pd.isna(row.get('shape_dist_traveled')) else None
        timepoint = Timepoint(row.get('timepoint')) if not pd.isna(row.get('timepoint')) else None
        pickup_booking_rule_id = str(row.get('pickup_booking_rule_id')) if not pd.isna(row.get('pickup_booking_rule_id')) else None
        drop_off_booking_rule_id = str(row.get('drop_off_booking_rule_id')) if not pd.isna(row.get('drop_off_booking_rule_id')) else None

        if trip_id is None:
            raise ValueError('Missing trip_id')
        if stop_sequence is None:
            raise ValueError('Missing stop_sequence')
        elif stop_sequence < 0:
                raise ValueError(f"Invalid stop_sequence {stop_sequence}. Must be non-negative")
        if shape_dist_traveled is not None:
             if shape_dist_traveled < 0:
                raise ValueError(f"Invalid shape_dist_traveled {shape_dist_traveled}. Must be non-negative")
                  
        return self(trip_id, arrival_time, departure_time, stop_id, location_group_id, location_id, stop_sequence, stop_headsign, start_pickup_drop_off_window, end_pickup_drop_off_window, pickup_type, drop_off_type, continuous_pickup, continuous_drop_off, shape_dist_traveled, timepoint, pickup_booking_rule_id, drop_off_booking_rule_id)
    
    def get_id(self) -> str:
        return self.trip_id