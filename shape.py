import pandas as pd
from dataclasses import dataclass

# Reference: https://gtfs.org/documentation/schedule/reference/#shapestxt
@dataclass(frozen=True)
class Shape:
    shape_id: str # Required
    shape_pt_lat: float # Required
    shape_pt_lon: float # Required
    shape_pt_sequence: int # Required
    shape_dist_traveled: float # Optional

    @classmethod
    def from_series(self, row: pd.Series):
        shape_id = str(row.get('shape_id')) if not pd.isna(row.get('shape_id')) else None
        shape_pt_lat = float(row.get('shape_pt_lat')) if not pd.isna(row.get('shape_pt_lat')) else None
        shape_pt_lon = float(row.get('shape_pt_lon')) if not pd.isna(row.get('shape_pt_lon')) else None
        shape_pt_sequence = int(row.get('shape_pt_sequence')) if not pd.isna(row.get('shape_pt_sequence')) else None
        shape_dist_traveled = float(row.get('shape_dist_traveled')) if not pd.isna(row.get('shape_dist_traveled')) else None

        if shape_id is None:
            raise ValueError('Missing shape_id')
        if shape_pt_lat is None:
            raise ValueError('Missing shape_pt_lat')
        if shape_pt_lon is None:
            raise ValueError('Missing shape_pt_lon')
        if shape_pt_sequence is None:
            raise ValueError('Missing shape_pt_sequence')
        elif shape_pt_sequence < 0:
                raise ValueError(f"Invalid shape_pt_sequence {shape_pt_sequence}. Must be non-negative")
        if shape_dist_traveled is not None:
             if shape_dist_traveled < 0:
                raise ValueError(f"Invalid shape_dist_traveled {shape_dist_traveled}. Must be non-negative")
                  
        return self(shape_id, shape_pt_lat, shape_pt_lon, shape_pt_sequence, shape_dist_traveled)
    
    def get_id(self) -> str:
        return self.shape_id