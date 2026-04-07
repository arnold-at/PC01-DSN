from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import os
import re
import uuid
import asyncio
from pathlib import Path

app = FastAPI(title="Instagram Reels Downloader", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent.parent
DOWNLOADS_DIR = BASE_DIR / "downloads"
DOWNLOADS_DIR.mkdir(exist_ok=True)

# Serve frontend static files
FRONTEND_DIR = BASE_DIR / "frontend"

class ReelRequest(BaseModel):
    url: str

def is_reel_url(url: str) -> bool:
    """Validate that the URL is an Instagram Reel (not a post or story)."""
    reel_patterns = [
        r"instagram\.com/reel/",
        r"instagram\.com/reels/",
    ]
    # Explicitly reject posts and stories
    reject_patterns = [
        r"instagram\.com/p/",       # posts
        r"instagram\.com/stories/", # stories
        r"instagram\.com/tv/",      # IGTV
    ]
    for pattern in reject_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return False
    for pattern in reel_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return True
    return False

def get_reel_info(url: str) -> dict:
    """Get reel metadata without downloading."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title", "Instagram Reel"),
            "duration": info.get("duration", 0),
            "thumbnail": info.get("thumbnail", ""),
            "uploader": info.get("uploader", "Unknown"),
            "view_count": info.get("view_count", 0),
            "like_count": info.get("like_count", 0),
            "description": info.get("description", ""),
        }

def download_reel(url: str, output_id: str) -> str:
    """Download the reel and return the file path."""
    output_path = DOWNLOADS_DIR / f"{output_id}.mp4"
    ydl_opts = {
        "outtmpl": str(DOWNLOADS_DIR / f"{output_id}.%(ext)s"),
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "quiet": True,
        "no_warnings": True,
        "merge_output_format": "mp4",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Find the downloaded file
    for f in DOWNLOADS_DIR.iterdir():
        if f.stem == output_id:
            return str(f)
    raise FileNotFoundError("Download failed")

@app.get("/")
async def serve_frontend():
    return FileResponse(FRONTEND_DIR / "index.html")

@app.post("/api/info")
async def get_info(request: ReelRequest):
    """Get reel metadata before downloading."""
    if not is_reel_url(request.url):
        raise HTTPException(
            status_code=400,
            detail="❌ URL no válida. Solo se permiten Reels de Instagram (instagram.com/reel/...)."
        )
    try:
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, get_reel_info, request.url)
        return JSONResponse(content={"success": True, "info": info})
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"No se pudo obtener información del Reel: {str(e)}")

@app.post("/api/download")
async def download(request: ReelRequest):
    """Download the Instagram Reel."""
    if not is_reel_url(request.url):
        raise HTTPException(
            status_code=400,
            detail="❌ URL no válida. Solo se permiten Reels de Instagram (instagram.com/reel/...)."
        )
    file_id = str(uuid.uuid4())
    try:
        loop = asyncio.get_event_loop()
        file_path = await loop.run_in_executor(None, download_reel, request.url, file_id)
        filename = Path(file_path).name
        return JSONResponse(content={
            "success": True,
            "file_id": file_id,
            "filename": filename,
            "download_url": f"/api/file/{filename}"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al descargar el Reel: {str(e)}")

@app.get("/api/file/{filename}")
async def serve_file(filename: str):
    """Serve the downloaded file."""
    # Sanitize filename
    filename = Path(filename).name
    file_path = DOWNLOADS_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=f"reel_{filename}",
        headers={"Content-Disposition": f"attachment; filename=reel_{filename}"}
    )

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "Instagram Reels Downloader"}

# Serve static files for frontend assets
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")