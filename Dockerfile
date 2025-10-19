# Use Python 3.9 slim as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service package
COPY service/ service/

# Create non-root user
RUN useradd -m -u 1000 theia

# Change ownership of /app to theia user
RUN chown -R theia:theia /app

# Switch to non-root user
USER theia

# Expose port 8080
EXPOSE 8080

# Use gunicorn as entry point
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "service:app"]
