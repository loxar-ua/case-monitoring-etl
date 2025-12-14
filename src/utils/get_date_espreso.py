from datetime import datetime, timezone

ukr_months = {
    "січня": "January",
    "лютого": "February",
    "березня": "March",
    "квітня": "April",
    "травня": "May",
    "червня": "June",
    "липня": "July",
    "серпня": "August",
    "вересня": "September",
    "жовтня": "October",
    "листопада": "November",
    "грудня": "December"
}

def parse_ukr_datetime(tag_date, tag_time):
    ukr_months = {
        "січня": 1, "лютого": 2, "березня": 3, "квітня": 4,
        "травня": 5, "червня": 6, "липня": 7, "серпня": 8,
        "вересня": 9, "жовтня": 10, "листопада": 11, "грудня": 12
    }
    date_text = tag_date.get_text(strip=True).split()
    day = int(date_text[0])
    month = ukr_months[date_text[1].strip(',')]
    year = int(date_text[2])
    hour, minute = map(int, tag_time.get_text(strip=True).split(':'))
    return (
        datetime(year, month, day, hour, minute, tzinfo=timezone.utc))
