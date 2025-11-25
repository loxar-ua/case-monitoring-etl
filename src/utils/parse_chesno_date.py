from datetime import datetime, timezone, timedelta

from bs4 import BeautifulSoup

UA_MONTHS = {
    "січня": 1, "лютого": 2, "березня": 3, "квітня": 4, "травня": 5, "червня": 6,
    "липня": 7, "серпня": 8, "вересня": 9, "жовтня": 10, "листопада": 11, "грудня": 12
}

def parse_chesno_date(element: BeautifulSoup) -> datetime:
    """Parses '11 липня 2024 р. 11:53' or '12 травня 11:34' into datetime."""

    if not element:
        return None

    date_str = str(element.text)

    # Clean up the string: "11 липня 2024 р. 11:53" -> "11 липня 2024 11:53"
    clean_str = date_str.replace(" р.", "").strip()

    try:
        parts = clean_str.split()
        day = int(parts[0])
        month_name = parts[1].lower()
        month = UA_MONTHS[month_name]

        if len(parts) == 4:
            year = int(parts[2])
            time_part = parts[3]
        elif len(parts) == 3:
            year = datetime.now().year
            time_part = parts[2]
        else:
            # Unknown format
            return None

        hour, minute = map(int, time_part.split(':'))

        dt = datetime(year, month, day, hour, minute)

        return dt.replace(tzinfo=timezone(timedelta(hours=2)))
    except (KeyError, ValueError, IndexError) as e:
        print(f"Date parsing error for '{date_str}': {e}") #TODO: log this
        return None

