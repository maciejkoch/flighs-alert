import sys
import os

# Add shared library to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi import FastAPI
import uvicorn
from api import health, root

app = FastAPI(title="Flights Alert API", version="0.1.0")

app.include_router(root.router)
app.include_router(health.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
