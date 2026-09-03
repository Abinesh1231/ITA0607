from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.database.database import init_db
from backend.app.api.routes import auth, waste, detection, classification, valuation, recommendations, dashboard

app = FastAPI(title=settings.APP_NAME, version="1.0.0", debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok", "service": settings.APP_NAME}

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(waste.router, prefix="/api/waste", tags=["Waste"])
app.include_router(detection.router, prefix="/api/detection", tags=["Detection"])
app.include_router(classification.router, prefix="/api/classification", tags=["Classification"])
app.include_router(valuation.router, prefix="/api/valuation", tags=["Valuation"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
