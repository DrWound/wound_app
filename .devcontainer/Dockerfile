FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y     build-essential     git     && rm -rf /var/lib/apt/lists/*

# Copy requirement files and install Python dependencies
COPY ../requirements.txt .

RUN pip install --upgrade pip &&     pip install -r requirements.txt

# Copy all project files (optional, may be adjusted)
COPY .. .

CMD ["bash"]
