import datetime as dt

from dateutil.parser import parse


def parse_date_if_exists(text: str = None) -> dt.date | None:
    """If the variable contains text with more than 5 characters, parse possible date."""
    if not text:
        return None
    elif text and len(text) < 5:
        return None
    elif not (parsed := parse(text)):
        return None
    return parsed.date()
