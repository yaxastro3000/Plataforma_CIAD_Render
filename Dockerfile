# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Define the command to run your application
CMD ["python", "DashVM.py"]
#CMD gunicorn -b 0.0.0.0:80 app:server
