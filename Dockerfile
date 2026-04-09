  
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
# Use Python 3.10 (compatible with torch 2.5.1)
# FROM python:3.10-slim
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git git-lfs ffmpeg libsm6 libxext6 cmake rsync libgl1 curl \
    && git lfs install \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies (with CPU torch support)
RUN pip install --no-cache-dir \
    -r /tmp/requirements.txt \
    -f https://download.pytorch.org/whl/torch_stable.html \
    gradio[oauth,mcp]==6.11.0 \
    "uvicorn[standard]" \
    "websockets>=10.4" \
    spaces

# Copy app files
COPY . .

# Run app
CMD ["python", "app.py"]