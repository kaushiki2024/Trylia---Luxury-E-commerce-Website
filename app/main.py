from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routes import auth, users, photos, outfits, sessions, recommendations


app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(photos.router)
app.include_router(outfits.router)
app.include_router(sessions.router)
app.include_router(recommendations.router)


@app.get("/")
def root():
    return {"message": "Trylia API is running"}


# Static serving for 3D files (if using local storage)
app.mount("/static", StaticFiles(directory="static"), name="static")

