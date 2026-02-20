# ---- Base image ----
FROM python:3.11-slim

# ---- Prevent python from writing pyc files ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Set working directory ----
WORKDIR /app

# ---- Install system deps (minimal) ----
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---- Copy requirements first (for caching) ----
COPY requirements.txt .

# ---- Install python deps ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project files ----
COPY . .

# ---- Expose FastAPI port ----
EXPOSE 8000

# ---- Start server ----
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
