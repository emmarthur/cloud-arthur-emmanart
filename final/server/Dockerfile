# Base image: Python 3.10
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements first for Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server.py .
COPY tools/ ./tools/

# Expose port 8080 (Cloud Run default)
EXPOSE 8080

# Run MCP server in HTTP mode
CMD ["python", "server.py"]


