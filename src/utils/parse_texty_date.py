from datetime import datetime, timezone


def parse_texty_date(element):
    if not element:
        return None

    date_str = str(element.text).strip()

    date_obj = datetime.strptime(date_str, "%Y-%m-%d%H:%M")

    date_obj_utc = date_obj.replace(tzinfo=timezone.utc)

    return date_obj_utc