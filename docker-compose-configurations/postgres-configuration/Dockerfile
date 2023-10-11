# We retrieve the official postgres image
FROM postgres:latest

# We copy the emikg_interfaces directory.
COPY ../../emikg_interfaces /app/emikg_interfaces

# We make sure that the pip version is up to date
RUN pip install --upgrade pip

# We install the emikg interfaces as a package
RUN pip install -e emikg_interfaces

# Start the postgres server
CMD ["postgres"]