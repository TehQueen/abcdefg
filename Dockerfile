# Stage 1: Base build stage
FROM python:3.13.3-alpine AS builder

# Create the app directory
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Upgrade pip and install dependencies
RUN pip install -U pip setuptools wheel

# Copy the requirements file first (better caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install -r requirements.txt

# Stage 2: Production stage
FROM python:3.13.3-alpine

RUN addgroup -S appgroup && \
    adduser -S -G appgroup appuser

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appgroup . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER appuser

RUN pybabel compile -d bot/locales -D messages

# Start the application
CMD ["python3", "-B", "-m", "bot"]
