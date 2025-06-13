# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=2.1.3

# Set working dir
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION"

# Copy only dependency files first for better caching
COPY pyproject.toml poetry.lock ./

# RUN pip install --upgrade pip && pip install poetry && poetry install --no-root
# Or if using pip only:
# RUN pip install --upgrade pip
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# Install project dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy rest of application
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
