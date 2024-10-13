# Use the official Python image as a base
FROM python:3.11-slim

# Install wkhtmltopdf dependencies
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy your Python script and any necessary files into the container
COPY . .

# Install the pdfkit library
RUN pip install pdfkit

# Command to run your Python script
CMD ["python", "your_script.py"]  # Change 'your_script.py' to your actual script name
