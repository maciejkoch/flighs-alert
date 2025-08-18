from fastapi import FastAPI
import uvicorn
from app.api import health, root

app = FastAPI()

app.include_router(root.router)
app.include_router(health.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
