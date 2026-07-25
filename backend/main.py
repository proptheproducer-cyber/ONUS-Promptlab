"""
ONUS PromptLab v2.0 — FastAPI Backend
Bridges the frontend and Suno's internal REST API.

Routes:
  GET  /                          → serves index.html
  POST /api/validate-cookie       → tests if a Suno cookie is valid
  POST /api/generate              → kicks off a Suno generation
  GET  /api/status/{song_id}      → polls a single song's status
  GET  /health                    → health check for Render.com
"""

import asyncio
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from backend.suno_client import SunoClient, SunoAuthError, SunoGenerationError

# ─── App setup ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="ONUS PromptLab API",
    version="2.0.0",
    docs_url="/docs",   # Available at /docs for debugging
)

# CORS — allow requests from the HTML frontend (same origin in prod, localhost in dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Tightened in production via env var if needed
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Path to the single HTML file — sits at repo root
INDEX_HTML = Path(__file__).parent.parent / "index.html"


# ─── Request / Response models ────────────────────────────────────────────────

class CookieRequest(BaseModel):
    cookie: str

class GenerateRequest(BaseModel):
    cookie: str
    title: str
    lyrics: str
    style: str
    model: Optional[str] = "chirp-v4"

class GenerateResponse(BaseModel):
    song_ids: list[str]
    message: str

class SongStatus(BaseModel):
    id: str
    title: str
    status: str                     # "queued" | "streaming" | "complete" | "error"
    audio_url: Optional[str]
    video_url: Optional[str]
    image_url: Optional[str]
    song_url: Optional[str]
    duration: Optional[float]
    tags: Optional[str]
    error_msg: Optional[str]


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/", include_in_schema=False)
async def serve_frontend():
    """Serve the main ONUS HTML app."""
    if not INDEX_HTML.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse(INDEX_HTML, media_type="text/html")


@app.get("/health")
async def health():
    """Render.com uses this to verify the container is alive."""
    return {"status": "ok", "version": "2.0.0"}


@app.post("/api/validate-cookie")
async def validate_cookie(req: CookieRequest):
    """
    Test whether a Suno cookie is valid before the user tries to generate.
    Returns account info (username, credits) on success.
    """
    if not req.cookie.strip():
        raise HTTPException(status_code=400, detail="Cookie cannot be empty.")
    try:
        client = SunoClient(req.cookie)
        info = await client.validate_cookie()
        return JSONResponse(content=info)
    except SunoAuthError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/api/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    """
    Submit a custom generation request to Suno.
    Returns song_ids immediately — poll /api/status/{id} for results.
    Generation takes 20–45 seconds; do NOT wait here.
    """
    if not req.cookie.strip():
        raise HTTPException(status_code=400, detail="Suno cookie is required.")
    if not req.lyrics.strip():
        raise HTTPException(status_code=400, detail="Lyrics cannot be empty.")
    if not req.style.strip():
        raise HTTPException(status_code=400, detail="Style tags cannot be empty.")

    try:
        client = SunoClient(req.cookie)
        song_ids = await client.generate(
            title=req.title or "ONUS Generated Track",
            lyrics=req.lyrics,
            style=req.style,
            model=req.model or "chirp-v4",
        )
        return GenerateResponse(
            song_ids=song_ids,
            message=f"Generation started. {len(song_ids)} track(s) queued.",
        )
    except SunoAuthError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except SunoGenerationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/api/status/{song_id}", response_model=list[SongStatus])
async def get_status(song_id: str, cookie: str):
    """
    Poll the status of one or more songs (comma-separated IDs).
    Called every 5 seconds by the frontend until status == 'complete'.

    Query params:
      cookie  — the user's Suno session cookie
    """
    if not cookie.strip():
        raise HTTPException(status_code=400, detail="Cookie query param is required.")

    ids = [s.strip() for s in song_id.split(",") if s.strip()]
    if not ids:
        raise HTTPException(status_code=400, detail="No valid song IDs provided.")

    try:
        client = SunoClient(cookie)
        songs = await client.get_songs(ids)
        return songs
    except SunoAuthError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except SunoGenerationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
