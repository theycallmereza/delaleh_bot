# Use an official Python runtime as the base image.
# https://hub.docker.com/_/python
FROM python:3.13

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev python3-dev && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements.txt file to the container.
COPY requirements.txt .

# Install the Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container.
COPY . .

# Set the default command to run the bot when the container starts.
CMD ["python", "-m", "src"]
