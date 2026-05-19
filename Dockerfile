# Dockerfile

# ── Base image ────────────────────────────────────────────
FROM python:3.11-slim

# ── Set working directory ─────────────────────────────────
WORKDIR /app

# ── Install dependencies first (better caching) ───────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy project files ────────────────────────────────────
COPY model/ ./model/
COPY app/ ./app/

# ── Expose port ───────────────────────────────────────────
EXPOSE 8000

# ── Start the API server ──────────────────────────────────
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]