# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Copy the software to the container at /app
COPY ./website /app/website

# Copy the run.py to the container at /app
COPY ./run.py /app/run.py

# We make sure that the pip version is up to date
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install -r /app/requirements.txt

# Run run.py when the container launches
CMD ["python", "/app/run.py"]