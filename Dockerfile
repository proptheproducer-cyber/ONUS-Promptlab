# ─── ONUS PromptLab v2.0 — Docker ─────────────────────────────────────────────
# FastAPI backend serves both the API and the static index.html
# Port 10000 = Render.com default for web services

FROM python:3.12-slim

# Install dependencies first (cached layer — only rebuilds if requirements change)
WORKDIR /app
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy the frontend (single file)
COPY index.html ./index.html

# Make sure Python finds the backend module
ENV PYTHONPATH=/app

# Render.com routes external traffic to port 10000
EXPOSE 10000

# Health check — Render uses this to decide if the deploy succeeded
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python -c "import httpx; httpx.get('http://localhost:10000/health').raise_for_status()"

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "10000"]
