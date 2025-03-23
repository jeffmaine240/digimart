from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Importing core app settings and route handlers
from core.config import config
from api.v1.routes import api_version_one

# App version
version = config.VERSION

# Creating FastAPI app instance with custom docs and versioning
app = FastAPI(
    title=config.APP_NAME,
    description=config.DESCRIPTION,
    version=version,
    openapi_url=f"/{version}/openapi.json",
    docs_url=f"/{version}/docs",
    redoc_url=f"/{version}/redoc",
)

# CORS Middleware to allow external connections (mobile apps, frontend, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allowed all domains 
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Including all API routes
app.include_router(api_version_one)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
