import os

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes.v1.routes import router as routesV1

load_dotenv()

app = FastAPI()

@app.get("/")
def ping():
    return {"status": "Service is Available"}

app.include_router(routesV1, prefix='/api/v1', tags=['v1.0.0'])

port = int(os.getenv("PORT", 7860))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)