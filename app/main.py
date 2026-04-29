from contextlib import asynccontextmanager

from fastapi import FastAPI

from .routers.register import v1_router

from .scheduler import scheduler, sweep_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    sweep_scheduler()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(v1_router)
