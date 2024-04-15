# Use the official Python image as a base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install webdriver_manager selenium

# Install Chromium and its dependencies
RUN apt-get update && apt-get install -y \
    chromium-browser \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libu2f-udev \
    libvulkan1 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils

# Set up environment for running Chromium headless
ENV DISPLAY=:99

# Copy the project files to the working directory in the container
COPY . /app/

# Run database migrations
RUN python manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "test_and_runserver", "0.0.0.0:8000"]
