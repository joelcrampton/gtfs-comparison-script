import pandas as pd
from dataclasses import dataclass
from datetime import date, datetime
from utils import check_email, check_url

# Reference: https://gtfs.org/documentation/schedule/reference/#feed_infotxt
@dataclass(frozen=True)
class FeedInfo:
    feed_publisher_name: str # Required
    feed_publisher_url: str # Required
    feed_lang: str # Required
    default_lang: str # Optional
    feed_start_date: date # Recommended
    feed_end_date: date # Recommended
    feed_version: str # Recommended
    feed_contact_email: str # Optional
    feed_contact_url: str # Optional

    @classmethod
    def from_series(self, row: pd.Series):
        feed_publisher_name = str(row.get('feed_publisher_name')) if not pd.isna(row.get('feed_publisher_name')) else None
        feed_publisher_url = str(row.get('feed_publisher_url')) if check_url(str(row.get('feed_publisher_url'))) else None
        feed_lang = str(row.get('feed_lang')) if not pd.isna(row.get('feed_lang')) else None
        default_lang = str(row.get('default_lang')) if not pd.isna(row.get('default_lang')) else None
        feed_start_date = datetime.strptime(str(row.get('feed_start_date')), "%Y%m%d").date() if not pd.isna(row.get('feed_start_date')) else None
        feed_end_date = datetime.strptime(str(row.get('feed_end_date')), "%Y%m%d").date() if not pd.isna(row.get('feed_end_date')) else None
        feed_version = str(row.get('feed_version')) if not pd.isna(row.get('feed_version')) else None
        feed_contact_email = str(row.get('feed_contact_email')) if check_email(str(row.get('feed_contact_email'))) else None
        feed_contact_url = str(row.get('feed_contact_url')) if check_url(str(row.get('feed_contact_url'))) else None

        if feed_publisher_name is None:
            raise ValueError('Missing feed_publisher_name')
        if feed_publisher_url is None:
            raise ValueError(f"Invalid feed_publisher_url '{feed_publisher_url}'")
        if feed_lang is None:
            raise ValueError('Missing feed_lang')
        
        return self(feed_publisher_name, feed_publisher_url, feed_lang, default_lang, feed_start_date, feed_end_date, feed_version, feed_contact_email, feed_contact_url)
    
    def get_id(self) -> str:
        return self.feed_publisher_name