from fastapi import FastAPI

app = FastAPI()


@app.get("/helloworld")
async def hello_world():
    return "Hello World!"
