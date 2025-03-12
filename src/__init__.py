from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import config


version = config.VERSION


app = FastAPI(
    title=config.APP_NAME,
    description=config.DESCRIPTION,
    version=version,
    openapi_url=f"/{version}/openapi.json",
    docs_url=f"/{version}/docs",
    redoc_url=f"/{version}/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)