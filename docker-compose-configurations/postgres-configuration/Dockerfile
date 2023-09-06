# We retrieve the official postgres image
FROM postgres:12.1

# Copy the initialization script into the container at /docker-entrypoint-initdb.d
COPY ./init.sql /docker-entrypoint-initdb.d/init.sql

# Start the postgres server
CMD ["postgres"]