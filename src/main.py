from fastapi import FastAPI, Header, HTTPException, Request
from datetime import datetime
import pytz
import json
from typing import Optional, Any, List

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
