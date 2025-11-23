from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.questions import router as questions_router
from config import get_settings
import dotenv

dotenv.load_dotenv()

settings = get_settings()
app = FastAPI(
    title="Car Rental Decision Tree API",
    description="AI-powered personalized car rental upgrade recommendations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(questions_router)


@app.get("/")
def root():
    return {"message": "Car Rental Decision Tree API", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
