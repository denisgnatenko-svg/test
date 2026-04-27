from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException, Query

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


@app.get("/time/convert")
def convert_time(
    dt: str = Query(..., description="ISO datetime, e.g. 2026-04-27T12:30:00"),
    from_tz: str = Query("UTC", description="IANA tz database name, e.g. Europe/Moscow"),
    to_tz: str = Query("UTC", description="IANA tz database name, e.g. America/New_York"),
) -> dict:
    raw = dt.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"

    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid dt: {e}") from e

    try:
        from_zone = ZoneInfo(from_tz)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid from_tz: {from_tz}") from e

    try:
        to_zone = ZoneInfo(to_tz)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid to_tz: {to_tz}") from e

    if parsed.tzinfo is None:
        src = parsed.replace(tzinfo=from_zone)
    else:
        src = parsed.astimezone(from_zone)

    dst = src.astimezone(to_zone)

    src_offset = src.utcoffset()
    dst_offset = dst.utcoffset()

    return {
        "input": {"dt": dt, "from_tz": from_tz, "to_tz": to_tz},
        "source": {
            "iso": src.isoformat(),
            "timezone": src.tzname(),
            "utc_offset_minutes": int((src_offset or 0).total_seconds() // 60),
            "unix_seconds": int(src.timestamp()),
        },
        "target": {
            "iso": dst.isoformat(),
            "timezone": dst.tzname(),
            "utc_offset_minutes": int((dst_offset or 0).total_seconds() // 60),
            "unix_seconds": int(dst.timestamp()),
        },
    }

