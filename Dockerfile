# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current project directory contents into the container at /app
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Define environment variable for Flask (tells Flask where your app.py is)
ENV FLASK_APP=app.py
# Make Flask accessible from outside the container (listen on all interfaces)
ENV FLASK_RUN_HOST=0.0.0.0

# Command to run the application when the container starts
CMD ["flask", "run"]