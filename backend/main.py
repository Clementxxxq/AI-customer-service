"""
Main FastAPI application
"""
import sys
from pathlib import Path

# Add backend directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from routes.services import router as services_router
from routes.doctors import router as doctors_router
from routes.customers import router as customers_router
from routes.chat import router as chat_router
from config.settings import (
    API_TITLE,
    API_VERSION,
    API_DESCRIPTION,
    CORS_ORIGINS,
    DEBUG
)

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    debug=DEBUG
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": API_VERSION}


# Include routers
app.include_router(services_router, prefix="/api/services")
app.include_router(doctors_router, prefix="/api/doctors")
app.include_router(customers_router, prefix="/api/customers")
app.include_router(chat_router, prefix="/api")


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    import sys
    from pathlib import Path
    
    # Add parent directory to path so uvicorn can find backend module
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )
