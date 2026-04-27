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

