from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from solo_plai.api.routes import games
from solo_plai.data.database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Solo Plai API",
    description="API for Solo Plai - AI-powered Warhammer: Age of Sigmar Spearhead opponent",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(games.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Solo Plai API",
        "docs": "/docs",
        "version": "0.1.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("solo_plai.main:app", host="0.0.0.0", port=8000, reload=True)
