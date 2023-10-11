# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

COPY requirements.txt /app

# Similarly, we copy the alchemy wrapper directory from the database.
COPY ../../postgres-configuration/alchemy_wrapper /app/alchemy_wrapper

# And the emikg interfaces.
COPY ../../emikg_interfaces /app/emikg_interfaces

# We make sure that the pip version is up to date
RUN pip install --upgrade pip

# We install the emikg interfaces as a package
RUN pip install -e emikg_interfaces

# We install the alchemy wrapper as a package
RUN pip install -e alchemy_wrapper

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run run.py when the container launches
CMD ["python", "/app/run.py"]
