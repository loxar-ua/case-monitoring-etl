import re
from datetime import datetime, timezone, timedelta
uk_months = {
    "січня": 1,
    "лютого": 2,
    "березня": 3,
    "квітня": 4,
    "травня": 5,
    "червня": 6,
    "липня": 7,
    "серпня": 8,
    "вересня": 9,
    "жовтня": 10,
    "листопада": 11,
    "грудня": 12,
}

def parse_uk_date(date_str: str) -> datetime:
    """
    Конвертує рядок виду '1 грудня, 00:08' у datetime з таймзоною +02:00
    """
    match = re.match(r"(\d+)\s+(\w+),\s*(\d+):(\d+)", date_str.strip())
    if not match:
        return None

    day, month_str, hour, minute = match.groups()
    month = uk_months.get(month_str.lower())
    if not month:
        return None

    return datetime(
        datetime.now().year,
        month,
        int(day),
        int(hour),
        int(minute),
        tzinfo=timezone(timedelta(hours=2))
    )
