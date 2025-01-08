from auto_poll import main
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/start")
async def start():
    main()
    return {"message": "Poll bot started"}