import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.upload_router import router as ingestion_router
from core.logging import logger
from core.lifecycle import lifespan

app = FastAPI(
    title = "Business Inteliigence",
    version = "1.0.0",
    lifespan=lifespan,
    description="Offline parsing engine extraction layer handling text, tables, and vision description assets."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion_router)

@app.get("/health", tags=["System Diagnostics"])
async def system_health_check():
    """Simple diagnostic endpoint to verify network availability."""
    return {"status": "healthy", "timestamp": uvicorn.config.Config.__name__}

if __name__ == "__main__":
    logger.info("Spinning up local development server on port 8000...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)