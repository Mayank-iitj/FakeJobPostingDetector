FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir gradio plotly requests

# Copy UI code
COPY ui/ ./ui/

# Expose Gradio port
EXPOSE 7860

# Run Gradio app
CMD ["python", "ui/gradio_app.py"]
