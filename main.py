from fastapi import FastAPI, HTTPException
from router import reservations, rooms
app = FastAPI(
    title="Meeting Room Booking API",
    description="A modular API for managing office space",
    version="1.0.0"
)

# Connect the routers
app.include_router(reservations.router)
app.include_router(rooms.router)

@app.get("/", tags=["Health"])
async def root():
    """Simple health check endpoint"""
    return {
        "status": "online",
        "message": "Welcome to the Meeting Room Booking API"
    }
