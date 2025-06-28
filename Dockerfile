# Dockerfile

# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit default port
EXPOSE 8501

# Set environment variables for Streamlit
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_PORT=8501 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false

# Run the Streamlit app
CMD ["streamlit", "run", "ui/app.py"]
