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

```bash
# 1. Clonar el repo
git clone https://github.com/tu-usuario/reels-downloader.git
cd reels-downloader

# 2. Construir la imagen
docker build -t reelgrab -f Dockerfile .

# 3. Correr
docker run -p 8000:8000 reelgrab
```

Abrir en el navegador: `http://localhost:8000`

## 🐳 Variantes de Docker

| Archivo | Descripción |
|---|---|
| `Dockerfile` | Básico, para desarrollo |
| `Dockerfile.optimizado` | Usuario no-root, 2 workers |
| `Dockerfile.multistage` | Virtualenv aislado, imagen más limpia |