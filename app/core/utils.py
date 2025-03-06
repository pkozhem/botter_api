import re
from datetime import UTC, datetime


def camel_to_snake(s: str) -> str:
    """Make camel case string to snake case string."""

    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    s = re.sub(r"__([A-Z])", r"_\1", s)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    s = s.lower()
    if s.endswith("y"):
        s = s[:-1] + "ie"
    return s


def utc_now() -> datetime:
    """Return now UTC datetime."""

    return datetime.now(UTC)
