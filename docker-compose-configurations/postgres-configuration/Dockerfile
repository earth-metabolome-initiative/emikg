# We retrieve the official postgres image
FROM postgres:latest

# We copy the enpkg_interfaces directory.
COPY ../../enpkg_interfaces /app/enpkg_interfaces

# We make sure that the pip version is up to date
RUN pip install --upgrade pip

# We install the enpkg interfaces as a package
RUN pip install -e enpkg_interfaces

# Start the postgres server
CMD ["postgres"]