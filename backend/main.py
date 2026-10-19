from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.database import init_db
from backend.routers import booking, procedures, staff

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(booking.router)
app.include_router(procedures.router)
app.include_router(staff.router)
