# Use an official Python runtime as a parent image
FROM python:3.8

# We expect the following environment variables to be set:
ARG YOUR_ORCID_CLIENT_ID
ARG YOUR_ORCID_CLIENT_SECRET

# We set the above arguments as environment variables
ENV YOUR_ORCID_CLIENT_ID=$YOUR_ORCID_CLIENT_ID
ENV YOUR_ORCID_CLIENT_SECRET=$YOUR_ORCID_CLIENT_SECRET

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r /app/requirements.txt

# Run app.py when the container launches
CMD ["python", "run.py"]