  
# FROM python:3.10-slim

# # Environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Install OS dependencies needed by uvicorn[standard]
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     gcc \
#     libffi-dev \
#     python3-dev \
#     && rm -rf /var/lib/apt/lists/*

# # Set working directory
# WORKDIR /app
# # ENV PYTHONPATH=/app/server
# ENV PYTHONPATH=/app

# # Copy requirements and install Python dependencies
# COPY requirements.txt /app/
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy all project code
# COPY . /app/

# # Expose FastAPI port
# EXPOSE 7860

# # Run FastAPI app
# # CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]

# # CMD ["uvicorn", "server.client:app", "--host", "0.0.0.0", "--port", "8000"]
# # CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
# # Use Python 3.10 (compatible with torch 2.5.1)


FROM python:3.11-slim

# Avoid Python cache + enable logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working dir
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Upgrade pip + install deps
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# HF Spaces expects this port
EXPOSE 7860

# Run app (IMPORTANT: dynamic port handled inside app.py)
CMD ["python","-m", "server/app.py"]