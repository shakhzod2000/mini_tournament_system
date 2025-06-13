# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working dir
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Install poetry if using it, otherwise use pip directly
COPY pyproject.toml .
COPY poetry.lock .  # if you use poetry
RUN pip install --upgrade pip && pip install poetry && poetry install --no-root

# Or if using pip only:
# RUN pip install --upgrade pip
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# Copy app
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
