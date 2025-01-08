from auto_poll import main
from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    main()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}