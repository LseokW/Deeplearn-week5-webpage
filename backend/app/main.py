from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.database import init_db
from app.routers import auth, content, payment


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="DeepLearn Week5 API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET_KEY)

app.include_router(auth.router)
app.include_router(content.router)
app.include_router(payment.router)


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "client_id_prefix": settings.GOOGLE_CLIENT_ID[:20] if settings.GOOGLE_CLIENT_ID else "EMPTY",
    }
