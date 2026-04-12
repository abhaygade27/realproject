FROM python:3.11-slim

# Avoid Python cache + enable logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Optimize installs (important for transformers/torch)
ENV PIP_NO_CACHE_DIR=1
ENV TRANSFORMERS_NO_TF=1
ENV TRANSFORMERS_NO_FLAX=1
ENV HF_HUB_DISABLE_SYMLINKS_WARNING=1

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy project files
COPY . .

# Expose port (HF Spaces requirement)
EXPOSE 7860

# Start FastAPI app
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]