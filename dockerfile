FROM python:3.9-slim

# Prevent Python buffering (important for Render)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (cache-friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Render default port
ENV PORT=10000
EXPOSE 10000

# Start FastAPI app
CMD ["uvicorn", "backend.api.app:app", "--host", "0.0.0.0", "--port", "10000"]
