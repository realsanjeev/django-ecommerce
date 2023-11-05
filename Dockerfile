# Use Python 3.9 as the base image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the contents of the current directory to /app in the container
COPY . /app

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Upgrade pip inside the virtual environment
RUN /opt/venv/bin/pip install pip --upgrade

# Install the requirements from requirements.txt
RUN /opt/venv/bin/pip install -r requirements.txt

# Run makemigrations and migrate
RUN /opt/venv/bin/python src/manage.py makemigrations &&\
    /opt/venv/bin/python src/manage.py migrate

# Expose port 8000
EXPOSE 8000

# Start the Django development server
CMD ["/opt/venv/bin/python", "src/manage.py", "runserver", "0.0.0.0:8000"]
