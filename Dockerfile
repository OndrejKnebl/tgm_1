# Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the necessary files into the container
COPY tgm_1.py .
COPY requirements.txt .

# Update and upgrade the system packages
RUN apt-get update && apt-get upgrade -y

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run tgm_1.py when the container launches
CMD ["python", "./tgm_1.py"]
