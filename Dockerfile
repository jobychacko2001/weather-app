# Use Alpine Linux as the base image
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
# RUN apk update \
#     && apk add --no-cache \
#         chromium \
#         chromium-chromedriver \
#         # Add any additional dependencies here \
#     && rm -rf /var/cache/apk/*

# Set up environment for running Chromium headless
ENV DISPLAY=:99

# Set working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the working directory in the container
COPY . /app/
COPY test_functional.py /app/weather_app/
# Run database migrations or other setup commands here if needed

# Expose the port the app runs on
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "test_and_runserver", "0.0.0.0:8000"]
