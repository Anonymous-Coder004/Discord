from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth,rooms,pdf
from app.sockets.router import register_ws_routes
def create_app() -> FastAPI:
    app = FastAPI(
        title="Discord-like Chat Platform",
        version="0.1.0",
    )

    # CORS (safe default for dev + prod)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
 
    # Health check (important for deployment)
    @app.get("/health")
    def health_check():
        return {"status": "ok"}
    
    app.include_router(auth.router)
    app.include_router(rooms.router)
    app.include_router(pdf.router)
    register_ws_routes(app)
    return app


app = create_app()

if(__name__=="__main__"):
    import uvicorn
    uvicorn.run(app="app.main:app",host="0.0.0.0",port=8000,reload=True)

