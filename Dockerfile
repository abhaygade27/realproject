FROM python:3.11-slim

# Avoid Python cache + enable logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Upgrade pip and install dependencies efficiently
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy project files
COPY . .

# Expose port (HF Spaces requirement)
EXPOSE 7860

# Start FastAPI app (make sure server/app.py defines `app`)
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
