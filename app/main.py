from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.dev_google_test import router as dev_google_test_router
from app.core.config import settings
from app.core.database import supabase_admin


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await supabase_admin.aclose()


app = FastAPI(
    title="FastAPI Auth System",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(dev_google_test_router)


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
