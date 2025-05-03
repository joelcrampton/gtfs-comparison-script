import pandas as pd
from dataclasses import dataclass
from enums import Continuous, RouteType
from utils import check_color, check_url

# Reference: https://gtfs.org/documentation/schedule/reference/#routestxt
@dataclass(frozen=True)
class Route:
    route_id: str # Required
    agency_id: str # Conditionally Required
    route_short_name: str # Conditionally Required
    route_long_name: str # Conditionally Required
    route_desc: str # Optional
    route_type: RouteType # Required
    route_url: str # Optional
    route_color: str # Optional
    route_text_color: str # Optional
    route_sort_order: int # Optional
    continuous_pickup: Continuous # Conditionally Forbidden
    continuous_drop_off: Continuous # Conditionally Forbidden
    network_id: str # Conditionally Forbidden

    @classmethod
    def from_series(self, row: pd.Series):
        route_id = str(row.get('route_id')) if not pd.isna(row.get('route_id')) else None
        agency_id = str(row.get('agency_id')) if not pd.isna(row.get('agency_id')) else None
        route_short_name = str(row.get('route_short_name')) if not pd.isna(row.get('route_short_name')) else None
        route_long_name = str(row.get('route_long_name')) if not pd.isna(row.get('route_long_name')) else None
        route_desc = str(row.get('route_desc')) if not pd.isna(row.get('route_desc')) else None
        route_type = RouteType(row.get('route_type')) if not pd.isna(row.get('route_type')) else None
        route_url = str(row.get('route_url')) if check_url(str(row.get('route_url'))) else None
        route_color = str(row.get('route_color')) if check_color(str(row.get('route_color'))) else None
        route_text_color = str(row.get('route_text_color')) if check_color(str(row.get('route_text_color'))) else None
        route_sort_order = int(row.get('route_sort_order')) if not pd.isna(row.get('route_sort_order')) else None
        continuous_pickup = Continuous(row.get('continuous_pickup')) if not pd.isna(row.get('continuous_pickup')) else Continuous.NO_CONTINUOUS
        continuous_drop_off = Continuous(row.get('continuous_drop_off')) if not pd.isna(row.get('continuous_drop_off')) else Continuous.NO_CONTINUOUS
        network_id = str(row.get('network_id')) if not pd.isna(row.get('network_id')) else None

        if route_id is None:
            raise ValueError('Missing route_id')
        if route_type is None:
            raise ValueError('Missing route_type')
        if route_sort_order is not None:
            if route_sort_order < 0:
                raise ValueError(f'Invalid route_sort_order {route_sort_order}. Must be non-negative')

        return self(route_id, agency_id, route_short_name, route_long_name, route_desc, route_type, route_url, route_color, route_text_color, route_sort_order, continuous_pickup, continuous_drop_off, network_id)
    
    def get_id(self) -> str:
        return self.route_id