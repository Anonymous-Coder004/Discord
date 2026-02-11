print("STEP 0: main.py module loading...")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

print("STEP 1: FastAPI imported")

# ---- SETTINGS ----
try:
    from app.core.config import settings
    print("STEP 2: settings imported successfully")
except Exception as e:
    print("ERROR during settings import:", e)
    raise

# ---- ROUTERS ----
try:
    from app.api import auth, rooms, pdf
    print("STEP 3: API routers imported")
except Exception as e:
    print("ERROR importing API routers:", e)
    raise

try:
    from app.sockets.router import register_ws_routes
    print("STEP 4: WebSocket router imported")
except Exception as e:
    print("ERROR importing WebSocket router:", e)
    raise


# ---- APP INIT ----
app = FastAPI(
    title="Discord-like Chat Platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

print("STEP 5: FastAPI app created")


# ---- MIDDLEWARE ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("STEP 6: CORS middleware added")


# ---- HEALTH CHECK ----
@app.get("/health")
def health_check():
    return {"status": "ok"}

print("STEP 7: Health route registered")


# ---- REGISTER ROUTERS ----
try:
    app.include_router(auth.router)
    print("STEP 8: Auth router registered")

    app.include_router(rooms.router)
    print("STEP 9: Rooms router registered")

    app.include_router(pdf.router)
    print("STEP 10: PDF router registered")

    register_ws_routes(app)
    print("STEP 11: WebSocket routes registered")

except Exception as e:
    print("ERROR during router registration:", e)
    raise


print("STEP 12: main.py fully loaded. Waiting for uvicorn to start...")
