"""Main application module for Resource Allocation AI System."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import Settings
from backend.core.db.database import engine
from backend.core.db import models

# Initialize models
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=Settings().PROJECT_NAME,
    openapi_url=f"{Settings().API_V1_STR}/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include API routers
# from backend.api.v1 import api_router
# app.include_router(api_router, prefix=Settings().API_V1_STR)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Resource Allocation AI System"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
