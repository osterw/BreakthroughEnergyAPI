from fastapi import FastAPI, Header, HTTPException, Request
from datetime import datetime
from typing import Optional, Any, List
import pytz
import json
import os
import subprocess
import hashlib
import hmac

app = FastAPI()


def flatten(data: Any) -> List[Any]:
    """Flatten a JSON entry into a list of keys and values"""
    result = []
    if isinstance(data, dict):
        for key, value in data.items():
            result.append(key)
            result.extend(flatten(value))
    elif isinstance(data, (list, tuple)):
        for item in data:
            result.extend(flatten(item))
    else:
        result.append(data)
    return result


def verify(body: bytes, signature: str) -> bool:
    webhook_secret = os.getenv("WEBHOOK_SECRET")
    if not webhook_secret:
        return True
    expected = hmac.new(
        webhook_secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


@app.get("/helloworld")
async def hello_world(
    tz: Optional[str] = None,
    accept: Optional[str] = Header(default="text/plain")
):
    message = "Hello World!"
    if tz:
        try:
            timezone = pytz.timezone(tz)
            current_time = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")
            message = f"{message} It is {current_time} in timezone: {tz}"
        except pytz.exceptions.UnknownTimeZoneError:
            raise HTTPException(status_code=400, detail=f"Your timezone {tz} is invalid")

    if accept == "application/json":
        return {"message": message}
    return message


@app.post("/unravel")
async def unravel_json(request: Request):
    try:
        body = await request.body()
        data = json.loads(body)
        return flatten(data)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=422,
            detail="Invalid JSON format"
        )


@app.post("/roll")
async def roll(request: Request):
    signature = request.headers.get('X-Hub-Signature-256', '')
    body = await request.body()
    if not verify(body, signature):
        raise HTTPException(status_code=401, detail="invalid signature")

    try:
        subprocess.run(["git", "pull", "origin", "main"], check=True)
        subprocess.run(["make", "restart"], check=True)
        return {"status": "success", "message": "Server updated and restarted"}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))
