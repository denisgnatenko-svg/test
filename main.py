from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="Time API", version="0.1.0")


@app.get("/")
def root() -> dict:
    return {"ok": True, "service": "time-api"}


@app.get("/time")
def get_time() -> dict:
    now_utc = datetime.now(timezone.utc)
    return {
        "server_time_utc": now_utc.isoformat(),
        "unix_seconds": int(now_utc.timestamp()),
        "timezone": "UTC",
    }


@app.get("/date")
def get_date() -> dict:
    now_utc = datetime.now(timezone.utc)
    return {
        "server_date_utc": now_utc.date().isoformat(),
        "timezone": "UTC",
    }


@app.get("/date/local")
def get_local_date() -> dict:
    now_local = datetime.now().astimezone()
    tz_name = now_local.tzinfo.tzname(now_local) if now_local.tzinfo else None
    return {
        "server_date_local": now_local.date().isoformat(),
        "timezone": tz_name,
        "utc_offset_minutes": int((now_local.utcoffset() or 0).total_seconds() // 60),
    }

