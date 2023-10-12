# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory to /app
WORKDIR /app

COPY enrichers/enricher-open-tree-of-life /app

# We copy the enrichers folder into the container at /app
COPY enrichers/enrichers /app/enrichers

# Similarly, we copy the alchemy wrapper directory from the database.
COPY postgres-configuration/alchemy_wrapper /app/alchemy_wrapper

# And then we copy the emikg interfaces
COPY emikg_interfaces /app/emikg_interfaces

# We make sure that the pip version is up to date
RUN pip install --upgrade pip

# We install the emikg interfaces
RUN pip install -e ./emikg_interfaces

# We install the alchemy wrapper package so to make it available to the run.py script
RUN pip install -e ./alchemy_wrapper

# We install the enrichers package so to make it available to the run.py script
RUN pip install -e ./enrichers

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run run.py when the container launches
CMD ["python", "run.py"]
