# Use the official Python image as a base
FROM python:3.11-slim

# Install wkhtmltopdf dependencies
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    libfontconfig1 \
    libxrender1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    

# Set the working directory
WORKDIR /app

# Copy your Python script and any necessary files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the outside world
EXPOSE 6000

# Step 7: Set environment variables to prevent Python from writing .pyc files and for Flask debugging
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=development

# Step 8: Command to run the Flask app
CMD ["python", "main.py"]
