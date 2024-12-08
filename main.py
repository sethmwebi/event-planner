from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from database.connection import conn
from routes.events import event_router
from routes.users import user_router


# Define the lifespan function
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    conn()
    yield  # Application runs here
    # Shutdown logic (if needed)
    print("App shutting down")


# Initialize FastAPI with lifespan
app = FastAPI(lifespan=lifespan)

# Register routes
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


@app.get("/")
async def home():
    return RedirectResponse(url="/event/")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
