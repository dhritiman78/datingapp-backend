import os

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes.user_route import router as user_router
from app.routes.reference_data_route import router as ref_router

load_dotenv()

app = FastAPI()

@app.get("/")
def ping():
    return {"status": "Service is Available"}

app.include_router(user_router, prefix='/user', tags=['User'])
app.include_router(ref_router, prefix='', tags=['Reference'])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)