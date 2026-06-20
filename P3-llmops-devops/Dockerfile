# Base Image
FROM python:3.10-slim as builder

WORKDIR /app

# Install system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final Runtime Image
FROM python:3.10-slim as runner

WORKDIR /app

# Copy dependencies installed via user path
COPY --from=builder /root/.local /root/.local
COPY . .

# Set environment paths
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Run FastAPI app
CMD ["python", "src/main.py"]
