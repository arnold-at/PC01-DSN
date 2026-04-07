# ============================================================
# Dockerfile — Versión básica / desarrollo
# Instagram Reels Downloader
# ============================================================

FROM python:3.12-slim

# Metadatos
LABEL maintainer="arnold-at"
LABEL description="Instagram Reels Downloader - Dockerfile básico"
LABEL version="1.0"

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Instalar dependencias del sistema (ffmpeg necesario para yt-dlp)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# Crear directorio de descargas
RUN mkdir -p downloads

# Cambiar al directorio del backend
WORKDIR /app/backend

# Exponer el puerto
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]