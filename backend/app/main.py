print("STEP 0: main.py file loading...")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

print("STEP 1: FastAPI imports done")

from app.core.config import settings
print("STEP 2: settings imported successfully")

from app.api import auth, rooms, pdf
print("STEP 3: routers imported successfully")

from app.sockets.router import register_ws_routes
print("STEP 4: websocket router imported successfully")

app = FastAPI(
    title="Discord-like Chat Platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

print("STEP 5: FastAPI app instance created")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("STEP 6: CORS middleware added")

@app.get("/health")
def health_check():
    return {"status": "ok"}

print("STEP 7: Health route registered")

app.include_router(auth.router)
print("STEP 8: Auth router registered")

app.include_router(rooms.router)
print("STEP 9: Rooms router registered")

app.include_router(pdf.router)
print("STEP 10: PDF router registered")

register_ws_routes(app)
print("STEP 11: WebSocket routes registered")

if __name__ == "__main__":
    print("STEP 12: Entered __main__ block")

    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    print(f"STEP 13: Starting uvicorn on port {port}")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port
    )
