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

# Copy the project files to the working directory in the container
COPY . /app/
COPY selenium_test.py /app/

# Run database migrations
RUN python manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Start the Django development server
#CMD ["python", "manage.py", "test_and_runserver", "0.0.0.0:8000"]

# Run selenium tests after starting the Django server
#CMD ["sh", "-c", "python3 selenium.py && exit 1 || exit 0"]
# Start the Django development server and run Selenium tests
CMD sh -c "python manage.py runserver 0.0.0.0:8000 & sleep 10; python3 selenium_test.py && exit 1 || exit 0"

