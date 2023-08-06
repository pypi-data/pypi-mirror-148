from datetime import date

import arrow
from dateutil.parser import parse


def format_full_date(text: str) -> date:
    """Gets a date with format February 2, 1911 and retrieves corresponding datetime object"""
    return arrow.get(text, "MMMM D, YYYY").date()


def parse_date_if_exists(text: str = None) -> date | None:
    """If the variable contains text with more than 5 characters, parse possible date."""
    if not text:
        return None
    elif text and len(text) < 5:
        return None
    elif not (parsed := parse(text)):
        return None
    return parsed.date()
