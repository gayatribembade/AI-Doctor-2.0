# Use official Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install system dependencies (for ffmpeg, pyaudio, etc.)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port Flask runs on
EXPOSE 8000

# Set environment variables (optional)
ENV FLASK_ENV=production

# Start the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
