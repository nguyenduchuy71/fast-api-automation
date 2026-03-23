from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import items, frontend, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")


app = FastAPI(
    title="My FastAPI App",
    description="A sample FastAPI application with Playwright tests",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(frontend.router)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello from FastAPI", "status": "ok"}


@app.get("/health", tags=["root"])
async def health():
    return {"status": "healthy"}
