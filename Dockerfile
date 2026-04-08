# Use Python slim image
FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install OS dependencies needed by uvicorn[standard]
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app
ENV PYTHONPATH=/app/server

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project code
COPY . /app/

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app
# CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]

# CMD ["uvicorn", "server.client:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
