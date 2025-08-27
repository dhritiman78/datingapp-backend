import os

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware  # ✅ Import CORSMiddleware

from app.routes.v1.routes import router as routesV1

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific domains like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.add_middleware(GZipMiddleware, minimum_size=100)

@app.get("/")
def ping():
    return {"status": "Service is Available"}

app.include_router(routesV1, prefix='/api/v1', tags=['v1.0.0'])

port = int(os.getenv("PORT", 7860))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)