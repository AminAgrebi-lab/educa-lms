# Base image: official Python 3.12.3 (Linux)
FROM python:3.12.3

# Do not write .pyc files inside the container
ENV PYTHONDONTWRITEBYTECODE=1
# Stream logs straight to the terminal without buffering
ENV PYTHONUNBUFFERED=1

# Working directory inside the image
WORKDIR /code

# Upgrade pip first
RUN pip install --upgrade pip

# Copy ONLY the requirements first: Docker caches this layer,
# so rebuilding after code changes stays fast
COPY requirements.txt .
RUN pip install -r requirements.txt

# Finally copy the whole project source code
COPY . .