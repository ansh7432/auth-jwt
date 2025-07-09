FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create staticfiles directory
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

RUN python manage.py migrate

# Expose port (8080 is the default for Cloud Run)
EXPOSE 8080

# Run the application using PORT environment variable (defaults to 8080 if not set)
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:${PORT:-8080}"]
