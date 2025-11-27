"""Timezone utilities for UTC+8 (Taiwan) conversion."""
from datetime import datetime, timedelta, timezone

# Taiwan timezone (UTC+8)
TZ_UTC8 = timezone(timedelta(hours=8))
TZ_UTC = timezone.utc


def utc_to_local(dt: datetime | None) -> datetime | None:
    """
    Convert UTC datetime to local time (UTC+8).

    This matches the Flask API behavior where database stores UTC
    and API returns UTC+8.
    """
    if dt is None:
        return None

    # If datetime is naive, assume UTC
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=TZ_UTC)

    return dt.astimezone(TZ_UTC8)


def local_to_utc(dt: datetime | None) -> datetime | None:
    """
    Convert local time (UTC+8) to UTC.

    Use this when receiving datetime from API and storing to database.
    """
    if dt is None:
        return None

    # If datetime is naive, assume local time (UTC+8)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=TZ_UTC8)

    return dt.astimezone(TZ_UTC)


def now_local() -> datetime:
    """Get current time in local timezone (UTC+8)."""
    return datetime.now(TZ_UTC8)


def now_utc() -> datetime:
    """Get current time in UTC."""
    return datetime.now(TZ_UTC)


def format_datetime(dt: datetime | None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime as string."""
    if dt is None:
        return ""
    return dt.strftime(fmt)


def parse_datetime(dt_str: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> datetime | None:
    """Parse datetime string."""
    if not dt_str:
        return None
    try:
        return datetime.strptime(dt_str, fmt)
    except ValueError:
        return None
