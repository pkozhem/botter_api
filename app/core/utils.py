from datetime import UTC, datetime


def utc_now() -> datetime:
    """Return now UTC datetime."""

    return datetime.now(UTC)
