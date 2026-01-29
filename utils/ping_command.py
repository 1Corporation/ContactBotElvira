import time
from datetime import timedelta
from aiogram.types import User

_STARTED_AT_MONO = time.monotonic()


def _format_uptime(seconds: float) -> str:
    td = timedelta(seconds=int(seconds))
    days = td.days
    hours, rem = divmod(td.seconds, 3600)
    minutes, secs = divmod(rem, 60)

    parts = []
    if days:
        parts.append(f"{days}д")
    if hours:
        parts.append(f"{hours}ч")
    if minutes:
        parts.append(f"{minutes}м")
    parts.append(f"{secs}с")
    return " ".join(parts)


def get_uptime() -> str:
    return _format_uptime(time.monotonic() - _STARTED_AT_MONO)


def build_ping_text(user: User | None) -> str:
    name = "друг"
    if user:
        name = (user.full_name or user.first_name or "друг").strip()

    return (
        f"Привет, {name}!\n"
        f"Я на связи.\n\n"
        f"🏓 Pong!\n"
        f"⏱ Аптайм: {get_uptime()}"
    )