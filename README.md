# 🎬 ReelGrab — Instagram Reels Downloader

Aplicación web para descargar Reels de Instagram en MP4.
Solo Reels — no Posts, no Stories, no IGTV.

## 🛠 Stack

- **Backend:** Python 3.12 + FastAPI
- **Descarga:** yt-dlp + FFmpeg
- **Frontend:** HTML + CSS + JavaScript

## 📁 Estructura
reels-downloader/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   └── index.html
├── downloads/
├── Dockerfile
├── Dockerfile.optimizado
└── Dockerfile.multistage

## 🚀 Cómo correrlo con Docker

**Requisito:** tener Docker instalado.

### Dockerfile básico
```bash
docker build -t reelgrab:basic -f Dockerfile .
docker run -p 8000:8000 reelgrab:basic
```
Abrir en el navegador: `http://localhost:8000`

### Dockerfile optimizado
```bash
docker build -t reelgrab:optimized -f Dockerfile.optimizado .
docker run -p 8001:8000 reelgrab:optimized
```
Abrir en el navegador: `http://localhost:8001`

### Dockerfile multistage
```bash
docker build -t reelgrab:multistage -f Dockerfile.multistage .
docker run -p 8002:8000 reelgrab:multistage
```
Abrir en el navegador: `http://localhost:8002`

## 🐳 Diferencia entre los Dockerfiles

| Archivo | Descripción |
|---|---|
| `Dockerfile` | Básico, ideal para desarrollo |
| `Dockerfile.optimizado` | Usuario no-root, 2 workers, más seguro |
| `Dockerfile.multistage` | Virtualenv aislado, imagen más limpia |