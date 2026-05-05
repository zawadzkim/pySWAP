# Use Python 3.11 slim image as base (force x86-64 for SWAP420 compatibility)
FROM --platform=linux/amd64 python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Copy requirements and install Python dependencies
COPY pyproject.toml ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root

# Copy pySWAP package
COPY pyswap/ ./pyswap/

# Copy SWAP420 Linux executable
COPY pyswap/libs/swap420-linux/swap420 /usr/local/bin/swap420
RUN chmod +x /usr/local/bin/swap420

# Set default command to keep container running
CMD ["bash"]
